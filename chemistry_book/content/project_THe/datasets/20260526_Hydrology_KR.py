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
# weather_station = '269'  # Lelystad: BB
weather_station = '350' # Kragge
pklfile = './DataFiles/meteo_KR.gz'

meteo_data_stat = dbl.download_meteoKNMI(t_range, weather_station, pklfile)
#meteo_data = meteo_data_stat.rename(columns={'rain': 'rain_station'})

# meteo_data is top boundary condition. We run the model from 2003 onward
meteo_data = meteo_data[slice(t_range[0], t_range[1])]

meteo_data.to_excel('df_meteo_KR.xlsx')

# %% read wastebody properties

cellIdx = 0  # KR3 = 0, KR4 = 1
lF_KR3 = dbl.wastebodyPropertiesKR(cellIdx)  # m2
#cellIdx = 1  # KR3 = 0, KR4 = 1
#lF_KR4 = dbl.wastebodyPropertiesKR(cellIdx)  # m2

#lF = pd.concat([lF_KR3,lF_KR4],axis=1)
#lF.columns=['KR3','KR4']


lF_KR3.to_excel('df_lF_KR.xlsx')

# %% 
# Download flow and level data from CHRONOS
## Index to sensor names in the data base
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



pklfiles = {'cumflow': './DataFiles/cumflow_dataKR.gz', 
            'flow': './DataFiles/flow_dataKR.gz',
            'level': './DataFiles/level_dataKR.gz',
            'infil': './DataFiles/cum_infildataKR.gz',
            'water_treatment': './DataFiles/water_treatmentKR.gz'}

cumflow_data, flow_data, level_data, cum_infil_data = \
    dbl.download_sens_data_Kragge (pklfiles)
# %%
# correct errors in flow data
cumflow_data = cumflow_data.rename(columns={'Flow_VP-06Cum': 'totalflow'})
totFvol = dbl.remove_outliers_inline(cumflow_data)
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