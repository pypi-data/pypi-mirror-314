import copy
import pandas as pd
import numpy as np
import xarray as xr
import os


DDF = os.path.join(os.path.dirname(__file__), '..', 'damage_assessment', 'supporting_data', 'damage_curves_and_values', 'DDF_Global.csv')


def apply_ddf(
    ds,
    ddfs=DDF
):
    ds = copy.deepcopy(ds)
    ddfs = pd.read_csv(ddfs)

    def depth_to_damage_percent(depth):
        return np.interp(depth, ddfs['Depth'], ddfs['Damage'])
    
    return xr.apply_ufunc(depth_to_damage_percent, ds)
