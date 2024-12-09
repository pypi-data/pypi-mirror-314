import numpy as np
import skrf as rf
import xarray as xr

HAM_BANDS = [
    [135.7e3, 137.8e3],
    [472e3, 479e3],
    [1.8e6, 2e6],
    [3.5e6, 4e6],
    [5332e3, 5405e3],
    [7e6, 7.3e6],
    [10.1e6, 10.15e6],
    [14e6, 14.35e6],
    [18.068e6, 18.168e6],
    [21e6, 21.45e6],
    [24.89e6, 24.99e6],
    [28e6, 29.7e6],
    [50e6, 54e6],
    [144e6, 148e6],
    [219e6, 220e6],
    [222e6, 225e6],
    [420e6, 450e6],
    [902e6, 928e6],
    [1240e6, 1300e6],
    [2300e6, 2310e6],
    [2390e6, 2450e6],
    [3400e6, 3450e6],
    [5650e6, 5925e6],
    [10e9, 10.5e9],
    [24e9, 24.25e9],
    [47e9, 47.2e9],
    [76e9, 81e9],
    [122.25e9, 123e9],
    [134e9, 141e9],
    [241e9, 250e9],
    [275e9, np.inf],
]


def db10(p):
    return 10 * np.log10(np.abs(p))


def db20(p):
    return 20 * np.log10(np.abs(p))


def minmax(x):
    return (np.min(x), np.max(x))


def s2net(s: xr.DataArray) -> rf.Network:
    net = rf.Network(frequency=s.frequency, f_unit="Hz", s=s)
    return net


def net2s(net: rf.Network) -> xr.DataArray:
    port_tuples = net.port_tuples

    m = list(set(t[0] for t in port_tuples))
    m.sort()
    m = np.array(m)
    m += 1  # skrf uses 0-indexed ports

    n = list(set(t[0] for t in port_tuples))
    n.sort()
    n = np.array(n)
    n += 1  # skrf uses 0-indexed ports

    s = xr.DataArray(
        net.s,
        dims=["frequency", "m", "n"],
        coords=dict(
            frequency=net.f,
            m=m,
            n=n,
        ),
    )
    return s
