from pathlib import Path

import skrf as rf
import xarray as xr
from util import net2s


# scikit-rf has no way to save files aside from touchstone and pickle
def cal2zarr(cal: rf.calibration.Calibration, outpath: Path):
    ideals = [net2s(net) for net in cal.ideals]
    measured = [net2s(net) for net in cal.measured]
    # s.to_zarr(outpath)
