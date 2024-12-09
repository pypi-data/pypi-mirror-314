# Charon

Named after [Pluto's moon](https://en.wikipedia.org/wiki/Charon_(moon)), Charon uses the [ADI Pluto SDR]() as a vector network analyzer. The basic usage is as a 1 port VNA but this can be extended to arbitrarily many ports with the addition of a couple RF switches.

## Installation

1. Install LibIIO. This is a dependency of [PyADI-IIO](https://wiki.analog.com/resources/tools-software/linux-software/pyadi-iio).
On Ubuntu 22.04 just run `sudo apt-get install -y libiio-dev`

2. `pip install charon-vna`

## Usage

There will be some sort of GUI because that sounds useful.
It will also be accessible over a socket to enable test automation with external (including non-python) code.

### Calibration

TBD

### Power Calibration
I include a default output power lookup table. This is derived from two TX channels of two Pluto SDRs and does not include any of the loss of a coupler or Charon switch board.

Absolute output power is generally not well calibrated for VNAs anyway and has negligible impact on most measurements so this is probably sufficient for most users. If you're trying to run a power sweep this may be insufficient.

If you have an RF power meter you can generate your own power calibration.

Note that unlike the main calibration, power calibration frequencies do not need to match the measurement frequencies. Values are interpolated.

## Hardware

You need a few things:
- [Analog Devices Pluto SDR](https://www.analog.com/en/resources/evaluation-hardware-and-software/evaluation-boards-kits/adalm-pluto.html).
Any variant of the Pluto *should* work too such as the [Pluto+](https://github.com/plutoplus/plutoplus?tab=readme-ov-file)
- Directional couplers (1 per port up to 4 ports).
I have been using [AAMCS-UDC-0.5G-18G-10dB-Sf](http://www.aa-mcs.com/wp-content/uploads/documents/AAMCS-UDC-0.5G-18G-10dB-Sf.pdf)
- Charon switch board - coming soon.
Without this, you'll be limited to S11 and uncalibrated S21 measurements (with required re-cabling).
There's nothing special about this particular board, if you want more than 4 ports you can make your own pretty easily. You just need 3 SPxT switches. Note that these switches will see tons of cycles so avoid mechanical switches.
- SMA cables

### Pluto Modification

We need two receive channels on the SDR. If you have a Pluto+ that should already be configured and you can skip this step.

Analog devices has a [guide](https://wiki.analog.com/university/tools/pluto/users/customizing#updating_to_the_ad9364) for enabling the second channel. Ideally this should be set as `ad9361` to enable a wider band of operation in addition to the second channel, however the critical setting is enabling 2r2t.