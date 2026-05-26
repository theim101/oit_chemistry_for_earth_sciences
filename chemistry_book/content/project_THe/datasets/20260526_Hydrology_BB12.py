# %%
import numpy as np
import scipy as sp
import pandas as pd
import DataBaseLibrary as dbl
import matplotlib.pyplot as plt
import seaborn as sns


#%matplotlib qt5
#sns.set()

# Define simulation time range and indentify time series with  with
# available mesaured data and
# the time over which we aim to calibrate the model


t_range = ['2003-01-01', '2026-04-01']

# %% 
# Meteo data
# Meteorological data will be obtained from two sources:
# 1: a close by weather station (for WM Berkhout, for BB: Lelystad)
#    we will use the evapotranspiration data obtained from the weather station...
# 2: rainfall from the 1km gridded radar corrected interpolated rainfall data obtained
#    from climate4impact...

# weather_station = '249'  # Berkhout
weather_station = '269'  # Lelystad: BB
# weather_station = '350' # Kragge
pklfile = './DataFiles/meteo_BB.gz'

meteo_data_stat = dbl.download_meteoKNMI(t_range, weather_station, pklfile)
#meteo_data = meteo_data_stat.rename(columns={'rain': 'rain_station'})

# meteo_data is top boundary condition. We run the model from 2003 onward
meteo_data = meteo_data[slice(t_range[0], t_range[1])]

# meteo_data.to_excel('df_meteo_BB.xlsx')
# %% read wastebody properties

# cellIdx = 0  # 'VP-06 = 0,'VP-05a = 1
cellIdx = 2  # 0 ='PP-11N',1='PP-11Z',2='PP-12']

lF = dbl.wastebodyPropertiesBB(cellIdx)  # m2

lF.to_excel('df_lF_BB12.xlsx')

# %% 
# Download flow and level data from CHRONOS
## Index to sensor names in the data base

pklfiles = {'cumflow': './DataFiles/cumflow_data_BB12.gz', 
            'level': './DataFiles/level_data_BB12.gz',
            }
sens_names = {'flowsens': 'Flow_PP-12Cum',
              'levelsens': 'Level_PP-12'}

cumflow_data, level_data = \
    dbl.download_sens_data_BB (pklfiles, sens_names)

# %%
# correct errors in flow data
cumflow_data = cumflow_data.rename(columns={'Flow_PP-12Cum': 'totalflow'})
totFvol = dbl.remove_outliers_inlineBB(cumflow_data)
totF = totFvol/lF.baseArea.values[0]

cumflow_data['totF'] = totF


# %%

# Define simulation time range (trange)
measFreq = 1
trange = pd.date_range(
    start=t_range[0],
    end = t_range[1],
    freq='D')

# As of pandas 3.0.0 change in default datetime64
if trange.dtype == '<M8[us]':
    units_per_sec = 1e6
else:
    units_per_sec = 1e9 

# %%
# We only require measured data that fall within the range of our simulation
# In addition we only require daily cumulative flow data
measFreq = 7
tmeas = pd.date_range(
    start='20120612', 
    end=t_range[1], 
    freq='7D')

finter = sp.interpolate.interp1d(cumflow_data['totF'].index.view(np.int64), 
                                 cumflow_data['totF'].values)
totF_val = finter(tmeas.view(np.int64))
totF_meas = pd.DataFrame(data=totF_val, index=tmeas)
totF_meas = totF_meas-totF_meas.iloc[0]
totF_meas = totF_meas.rename(columns={0: 'cum_Leachate'})

totF_meas.to_excel('df_cumLeachate_BB12.xlsx')
# %%