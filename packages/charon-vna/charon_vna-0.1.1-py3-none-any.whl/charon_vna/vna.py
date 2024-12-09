# %% imports
import copy
from pathlib import Path
from typing import Any, Dict, Tuple

import adi
import iio
import numpy as np
import skrf as rf
import xarray as xr
from matplotlib import pyplot as plt
from matplotlib.ticker import EngFormatter
from numpy import typing as npt
from scipy import signal
from util import HAM_BANDS, db20, net2s, s2net

dir_ = Path(__file__).parent


# %% connection


def generate_tone(f: float, fs: float, N: int = 1024, scale: int = 2**14):
    fs = int(fs)
    fc = int(f / (fs / N)) * (fs / N)
    ts = 1 / float(fs)
    t = np.arange(0, N * ts, ts)
    i = np.cos(2 * np.pi * t * fc) * scale
    q = np.sin(2 * np.pi * t * fc) * scale
    iq = i + 1j * q

    return iq


class Charon:
    FREQUENCY_OFFSET = 1e6

    def __init__(
        self,
        uri: str,
        frequency: npt.ArrayLike = np.linspace(1e9, 2e9, 3),
        ports: Tuple[int] = (1,),
    ):
        self.ports = ports
        self.frequency = frequency

        # everything RF
        self.sdr = adi.ad9361(uri=uri)
        for attr, expected in [
            ("adi,2rx-2tx-mode-enable", True),
            # ("adi,gpo-manual-mode-enable", True),
        ]:
            # available configuration options:
            # https://wiki.analog.com/resources/tools-software/linux-drivers/iio-transceiver/ad9361-customization
            if bool(self.sdr._get_iio_debug_attr(attr)) != expected:
                raise ValueError(
                    f"'{attr}' is not set in pluto. "
                    "See README.md for instructions for one time configuration instructions"
                )
                # TODO: it might be possible to change this on the fly.
                # I think we'll actually just fail in __init__ of ad9361 if 2rx-2tx is wrong

        self.sdr.rx_lo = int(self.frequency[0])
        self.sdr.tx_lo = int(self.frequency[0])
        self.sdr.sample_rate = 30e6
        self.sdr.rx_rf_bandwidth = int(4e6)
        self.sdr.tx_rf_bandwidth = int(4e6)
        self.sdr.rx_destroy_buffer()
        self.sdr.tx_destroy_buffer()
        self.sdr.rx_enabled_channels = [0, 1]
        self.sdr.tx_enabled_channels = [0]
        self.sdr.loopback = 0
        self.sdr.gain_control_mode_chan0 = "manual"
        self.sdr.gain_control_mode_chan1 = "manual"
        self.sdr.rx_hardwaregain_chan0 = 10
        self.sdr.rx_hardwaregain_chan1 = 10
        self.sdr.tx_hardwaregain_chan0 = -10

        # # switch control
        # ctx = iio.Context(uri)
        # self.ctrl = ctx.find_device("ad9361-phy")
        # # raw ad9361 register accesss:
        # # https://ez.analog.com/linux-software-drivers/f/q-a/120853/control-fmcomms3-s-gpo-with-python
        # # https://www.analog.com/media/cn/technical-documentation/user-guides/ad9364_register_map_reference_manual_ug-672.pdf
        # self.ctrl.reg_write(0x26, 0x90)  # bit 7: AuxDAC Manual, bit 4: GPO Manual
        # self._set_gpo(self.ports[0] - 1)
        # # TODO: init AuxDAC

    def get_config(self) -> Dict[str, Any]:
        config = dict()
        config["rx_lo"] = self.sdr.rx_lo
        config["rx_rf_bandwidth"] = self.sdr.rx_rf_bandwidth
        config["rx_enabled_channels"] = self.sdr.rx_enabled_channels
        for chan in config["rx_enabled_channels"]:
            config[f"rx_hardwaregain_chan{chan}"] = getattr(self.sdr, f"rx_hardwaregain_chan{chan}")
            config[f"gain_control_mode_chan{chan}"] = getattr(self.sdr, f"gain_control_mode_chan{chan}")

        config["tx_lo"] = self.sdr.tx_lo
        config["tx_rf_bandwidth"] = self.sdr.tx_rf_bandwidth
        config["tx_cyclic_buffer"] = self.sdr.tx_cyclic_buffer
        config["tx_enabled_channels"] = self.sdr.tx_enabled_channels
        for chan in config["tx_enabled_channels"]:
            config[f"tx_hardwaregain_chan{chan}"] = getattr(self.sdr, f"tx_hardwaregain_chan{chan}")

        config["filter"] = self.sdr.filter
        config["sample_rate"] = self.sdr.sample_rate
        config["loopback"] = self.sdr.loopback

        return config

    def _get_gpo(self) -> int:
        return (self.ctrl.reg_read(0x27) >> 4) & 0x0F

    def _set_gpo(self, value: int) -> None:
        self.ctrl.reg_write(0x27, (value & 0x0F) << 4)  # bits 7-4: GPO3-0

    def set_output_power(self, power: float):
        # FIXME: this is a hack because I don't want to go through re-calibration
        if power == 5:
            tx_gain = -1
        elif power == 0:
            tx_gain = -7
        elif power == -5:
            tx_gain = -12
        elif power == -10:
            tx_gain = -17
        elif power == -15:
            tx_gain = -22
        else:
            raise NotImplementedError()
            # # TODO: correct over frequency
            # tx_gain_idx = np.abs(pout.sel(tx_channel=0) - power).argmin(dim="tx_gain")
            # tx_gain = pout.coords["tx_gain"][tx_gain_idx]
        self.sdr.tx_hardwaregain_chan0 = float(tx_gain)

    def set_output(self, frequency: float, power: float):
        # TODO: switch to DDS in Pluto

        self.sdr.tx_destroy_buffer()
        self.set_output_power(power)
        self.sdr.tx_lo = int(frequency - self.FREQUENCY_OFFSET)
        self.sdr.tx_cyclic_buffer = True
        # self.sdr.tx(generate_tone(f=self.FREQUENCY_OFFSET, fs=self.sdr.sample_rate))
        self.sdr.dds_single_tone(self.FREQUENCY_OFFSET, scale=0.9, channel=0)

    def _rx(self, count: int = 1, fc: float | None = None) -> npt.ArrayLike:
        if count < 1:
            raise ValueError

        self.sdr.rx_destroy_buffer()
        if fc is not None:
            self.sdr.rx_lo = int(fc)
        self.sdr.rx_enabled_channels = [0, 1]
        self.sdr.gain_control_mode_chan0 = "manual"
        self.sdr.gain_control_mode_chan1 = "manual"
        self.sdr.rx_hardwaregain_chan0 = 30
        self.sdr.rx_hardwaregain_chan1 = 30
        return np.concatenate([np.array(self.sdr.rx()) for _ in range(count)], axis=-1)

    def get_b_over_a(self, frequency: float):
        self.set_output(frequency=frequency, power=-5)

        data = self._rx(1, fc=frequency - self.FREQUENCY_OFFSET)
        ddc_tone = generate_tone(f=-self.FREQUENCY_OFFSET, fs=self.sdr.sample_rate, scale=1)
        ddc_data = data * ddc_tone

        ddc_rel = ddc_data[1] / ddc_data[0]

        # plt.figure()
        # plt.plot(
        #     np.fft.fftshift(np.fft.fftfreq(ddc_data.shape[-1], 1 / self.sdr.sample_rate)),
        #     np.abs(np.fft.fftshift(np.fft.fft(ddc_data, axis=-1))).T,
        # )
        # plt.show()

        # TODO: calculate sos only once
        n, wn = signal.buttord(
            wp=0.3 * sdr.FREQUENCY_OFFSET,
            ws=0.8 * sdr.FREQUENCY_OFFSET,
            gpass=1,
            gstop=40,
            analog=False,
            fs=self.sdr.sample_rate,
        )
        sos = signal.butter(n, wn, "lowpass", analog=False, output="sos", fs=self.sdr.sample_rate)
        # TODO: figure out why filt sucks. Introduces SO much phase noise (out to several MHz)
        filt_data = signal.sosfiltfilt(sos, ddc_data, axis=-1)

        filt_rel = filt_data[1] / filt_data[0]

        return np.mean(data[1] / data[0])

    def sweep_b_over_a(self):
        s = xr.DataArray(
            np.zeros(
                len(self.frequency),
                dtype=np.complex128,
            ),
            dims=["frequency"],
            coords=dict(
                frequency=self.frequency,
            ),
        )
        for frequency in self.frequency:
            s.loc[dict(frequency=frequency)] = self.get_b_over_a(frequency=frequency)
        return s

    def vna_capture(self, frequency: npt.ArrayLike):
        s = xr.DataArray(
            np.empty(len(frequency), dtype=np.complex128),
            dims=["frequency"],
            coords=dict(
                frequency=frequency,
            ),
        )
        for freq in s.frequency.data:
            self.set_output(frequency=freq, power=-5)
            self.sdr.rx_destroy_buffer()
            self.sdr.rx_lo = int(freq)
            self.sdr.rx_enabled_channels = [0, 1]
            self.sdr.gain_control_mode_chan0 = "manual"
            self.sdr.gain_control_mode_chan1 = "manual"
            self.sdr.rx_hardwaregain_chan0 = 40
            self.sdr.rx_hardwaregain_chan1 = 40
            rx = self.sdr.rx()
            s.loc[dict(frequency=freq)] = np.mean(rx[1] / rx[0])

        return s


# %%
sdr = Charon("ip:192.168.3.1", frequency=np.linspace(1e9, 1.1e9, 11))

# %% initialization
config = sdr.get_config()
# print(sdr.ctrl.debug_attrs["adi,rx-rf-port-input-select"].value)
# print(sdr.ctrl.debug_attrs["adi,tx-rf-port-input-select"].value)
config

# %% generate tone
fc = 1e9
sdr.set_output(frequency=fc + sdr.FREQUENCY_OFFSET, power=-5)

# %% capture data
data = sdr._rx(1, fc=fc)

# %% Plot in time
fig, axs = plt.subplots(2, 1, sharex=True, tight_layout=True)
axs[0].plot(np.real(data).T)
axs[1].plot(np.imag(data).T)
axs[0].set_ylabel("Real")
axs[1].set_ylabel("Imag")
axs[0].grid(True)
axs[1].grid(True)
axs[-1].set_xlabel("Sample")
axs[-1].set_xlim(0, data.shape[-1])
fig.show()

# %%
fig, ax = plt.subplots(1, 1, tight_layout=True)
ax.plot(np.real(data).T, np.imag(data).T)
ax.grid(True)
ax.set_aspect("equal")
ax.set_xlabel("Real")
ax.set_ylabel("Imag")
ax.set_xlim(np.array([-1, 1]) * (2 ** (12 - 1) - 1))
ax.set_ylim(ax.get_xlim())
fig.show()

# %% Plot in frequency
f = np.fft.fftfreq(data.shape[-1], 1 / sdr.sdr.sample_rate)
RX_BITS = 12  # for each of i, q (including sign bit)
fft_data = np.fft.fft(data, axis=-1, norm="forward") / (2 ** (RX_BITS - 1))
plt.figure()
for cc, chan in enumerate(sdr.sdr.rx_enabled_channels):
    plt.plot(
        np.fft.fftshift(f),
        db20(np.fft.fftshift(fft_data[cc])),
        label=f"Channel {chan}",
    )
plt.legend()
plt.ylim(-100, 0)
plt.xlabel("Frequency [Hz]")
plt.ylabel("Power [dBfs]")
plt.title(f"Fc = {sdr.sdr.rx_lo / 1e9} GHz")
plt.gca().xaxis.set_major_formatter(EngFormatter())
plt.grid(True)
plt.show()


# %%
s = sdr.vna_capture(frequency=np.linspace(70e6, 200e6, 101))

# %% Plot Logmag
fig, axs = plt.subplots(2, 1, sharex=True, tight_layout=True)

axs[0].plot(s.frequency, db20(s), label="Measured")
axs[1].plot(s.frequency, np.rad2deg(np.angle((s))), label="Measured")

axs[0].grid(True)
axs[1].grid(True)

axs[0].set_ylim(-80, 0)
axs[1].set_ylim(-200, 200)
axs[1].set_xlim(np.min(s.frequency), np.max(s.frequency))
axs[1].xaxis.set_major_formatter(EngFormatter(places=1))
axs[1].set_xlabel("Frequency")

axs[0].set_ylabel("|S11| [dB]")
axs[1].set_ylabel("∠S11 [deg]")

reference_sparams = None
reference_sparams = dir_ / "RBP-135+_Plus25degC.s2p"
if reference_sparams is not None:
    ref = rf.Network(reference_sparams)
    rbp135 = net2s(ref)

    axs[0].plot(rbp135.frequency, db20(rbp135.sel(m=1, n=1)), label="Datasheet")
    axs[1].plot(rbp135.frequency, np.rad2deg(np.angle(rbp135.sel(m=2, n=1))), label="Datasheet")
    axs[0].legend()
    axs[1].legend()

plt.show()


# %% SOL calibration
cal_frequency = np.linspace(70e6, 600e6, 101)
ideal_cal_frequency = rf.Frequency(np.min(cal_frequency), np.max(cal_frequency), len(cal_frequency))
input("Connect SHORT and press ENTER...")
short = sdr.vna_capture(frequency=cal_frequency)
input("Connect OPEN and press ENTER...")
open = sdr.vna_capture(frequency=cal_frequency)
input("Connect LOAD and press ENTER...")
load = sdr.vna_capture(frequency=cal_frequency)

short_net = s2net(short)
open_net = s2net(open)
load_net = s2net(load)

cal_ideal = rf.media.DefinedGammaZ0(frequency=ideal_cal_frequency)
calibration = rf.calibration.OnePort(
    [short_net, open_net, load_net],
    [cal_ideal.short(), cal_ideal.open(), cal_ideal.load(0)],
)


# %%
s = sdr.vna_capture(frequency=cal_frequency)

# %%
s_calibrated = calibration.apply_cal(s2net(s))

plt.figure()
s_calibrated.plot_s_smith()
# ref.plot_s_smith(m=1, n=1)
plt.show()

plt.figure()
for start, stop in HAM_BANDS:
    plt.axvspan(start, stop, alpha=0.1, color="k")
s_calibrated.plot_s_db()
# ref.plot_s_db(m=1, n=1)
plt.gca().xaxis.set_major_formatter(EngFormatter())
plt.grid(True)
plt.xlim(s_calibrated.f[0], s_calibrated.f[-1])
plt.show()

plt.figure()
for start, stop in HAM_BANDS:
    plt.axvspan(start, stop, alpha=0.1, color="k")
# s_calibrated.plot_s_vswr()
# drop invalid points
vswr = copy.deepcopy(s_calibrated.s_vswr[:, 0, 0])
vswr[vswr < 1] = np.nan
plt.plot(s_calibrated.f, vswr)
plt.axhline(1, color="k", linestyle="--")
plt.ylabel("VSWR")
plt.xlabel("Frequency [Hz]")
# ref.plot_s_vswr(m=1, n=1)
plt.gca().xaxis.set_major_formatter(EngFormatter())
plt.grid(True)
plt.ylim(0, 10)
plt.xlim(s_calibrated.f[0], s_calibrated.f[-1])
plt.show()

# %%
