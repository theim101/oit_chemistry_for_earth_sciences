# import libraries and prepare for plotting 
#!/usr/bin/env python
# coding: utf-8

# # Time series for the Kragge landfill
# 

# In[1]:


# Import the python packages needed to connect to the database and process the data
import sqlalchemy as sa
import scipy as sp
import numpy as np
#import pandas as pd
import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns
import os
import zipfile
import datetime as dt

from IPython.display import Markdown, display

#get_ipython().run_line_magic('matplotlib', 'widget')
sns.set() # For the seaborn default
%matplotlib qt

# %% 1
# Setup the connection to the database
conn_str = 'mysql+pymysql://Guest_01:TUDelft01@localhost:3307/database_iDS05'
db_engine = sa.create_engine(conn_str)

measpoint_name_list = (
    "('BoZ.PP-1', 'BoZ.PP-2', 'BoZ.PP-3', 'BoZ.PP-4', "
    "'BoZ.PP-V2', 'BoZ.PP-V3', 'BoZ.PP-V4', 'BoZ.PP-V5', "
    "'BoZ.CWZI', 'BoZ.CWZI-inf', 'BoZ.CWZI-eff', "
    "'PP-11N', 'PP-11Z', 'PP-12', "
    "'VP-06', 'IDS-put 6')"
)

# select the data for the different sensors per group
# Cumulative Flow data
sql_query = (
    "select mp.compartment, mp.measpointname , s.date, "
        "a.par_description, c.name_nl as cname, a.detectlim, a.value, "
        "u.name_nl as uname, m.`type` "
    "from measurement_point mp, sample s, analysis a, component c , unit u, `method` m "  
    "where mp.measpointno = s.measpointno "
    "and a.sampleno = s.sampleno "
    "and c.componentno = a.componentno "
    "and u.unitno = a.unitno "
    "and m.methodno = a.methodno "
    "and m.methodno in (1,2) "
    "and mp.measpointname in " + measpoint_name_list + " "
)
        
#import the data in to a dataframe
df_lab_all = pl.read_database(
    query=sql_query, 
    connection=db_engine.connect(),
    schema_overrides={
        "par_description": pl.String,
        "detectlim": pl.String,
        }
)

# df_lab_all.write_excel('df_lab_all_manual.xlsx')
# %% 2
# Renames the measpointname VP-06 to IDS-put 6 as they are the same sampling point
df_lab_all = df_lab_all.with_columns(
    pl.when(pl.col('measpointname') == 'VP-06')
    .then(pl.lit('IDS-put 6'))
    .otherwise(pl.col('measpointname'))
    .alias('measpointname')
)

# %%
# Some names are double but slightly different 
# (e.g. Ammonium (als NH4) and Ammonium (als N)), 
# We will move all to one name:
# Ammonium (als NH4) and Ammonium (als N) will be merged into 'Ammonium'.
# Fosfaat (als P2O5), Fosfaat (als PO4) and Fosfaat (totaal, als P2O5) will be merged into 'Fosfaat (totaal)'.
# Fluoride and Fluoride (totaal) will be merged into 'Fluoride (totaal)',
# Zwavel (totaal, als SO4) will be merged into 'Sulfaat (als SO4)',
# Geleidendheid, Geleidbaarheid (20Â°C) and Geleidbaarheid (25Â°C) will be merged into 'Geleidbaarheid'.

#    'Fosfaat (als P2O5)', 'Fosfaat (als PO4)', 'Fosfaat (totaal, als P2O5)'

NH4_N_ratio = 18.039 / 14.007  # MW(NH4) / MW(N)
PO4_P_ratio = 94.971 / 30.974  # MW(PO4) / MW(P)
PO4_P2O5_ratio = 30.974 / 141.94  # MW(P2O5) / MW(P)
SO4_S_ratio = 96.06 / 32.06  # MW(SO4) / MW(S)

df_lab_all = df_lab_all.with_columns([
    pl.when(pl.col('cname').is_in ([
        'Ammonium (als N)', 'Ammonium'
    ]))
    .then(pl.lit('Ammonium (als NH4)'))
    .otherwise(pl.col('cname'))
    .alias('cname'),

    pl.when(pl.col('cname') == 'Ammonium (als N)')
    .then(pl.col('value') * NH4_N_ratio)
    .otherwise(pl.col('value'))
    .alias('value')
])

df_lab_all = df_lab_all.with_columns([
    pl.when(pl.col('cname').is_in ([
        'Fosfor (als PO4)',
        '2-Fosfaat (als PO4) (ortho-Fosfaat (als PO4))',
        ]))
    .then(pl.lit('Fosfaat (als PO4)'))
    .otherwise(pl.col('cname'))
    .alias('cname'),
])


df_lab_all = df_lab_all.with_columns([
    pl.when(pl.col('cname').is_in ([
        'Fosfaat (als P2O5)', 
        'Fosfaat (totaal, als P2O5)',
        ]))
    .then(pl.lit('Fosfaat (als PO4)'))
    .otherwise(pl.col('cname'))
    .alias('cname'),

    pl.when(pl.col('cname').is_in([
        'Fosfaat (als P2O5)', 
        'Fosfaat (totaal, als P2O5)'
        ]))
    .then(pl.col('value') * PO4_P2O5_ratio)
    .otherwise(pl.col('value'))
    .alias('val_mgl'),
])

df_lab_all = df_lab_all.with_columns([
    pl.when(pl.col('cname').is_in([
        'Fosfaat (als P)', 'Fosfor [P]'
        ]))
    .then(pl.lit('Fosfaat (als PO4)'))
    .otherwise(pl.col('cname'))
    .alias('cname'),

    pl.when(pl.col('cname').is_in([
        'Fosfaat (als P)', 'Fosfor [P]'
        ]))
    .then(pl.col('value') * PO4_P_ratio)
    .otherwise(pl.col('value'))
    .alias('value')
])

df_lab_all = df_lab_all.with_columns([
    pl.when(pl.col('cname').is_in([
        'Sulfaat (opgelost, als S)',
        'Zwavel (totaal, als SO4)'
        ]))
    .then(pl.lit('Sulfaat (als SO4)'))
    .otherwise(pl.col('cname'))
    .alias('cname'),
    
    pl.when(pl.col('cname')== 'Sulfaat (opgelost, als S)')
    .then(pl.col('value') * SO4_S_ratio)
    .otherwise(pl.col('value'))
    .alias('value')
])

df_lab_all = df_lab_all.with_columns([
    pl.when(pl.col('cname')=='Geleidendheid')
        .then(pl.lit('Geleidbaarheid (25Â°C)'))
        .otherwise(pl.col('cname'))
        .alias('cname')
])


# %% 3
# Ensure that all units are in mg/L or mS/cm

df_lab_all = (
    df_lab_all
    .with_columns(
        pl.when(pl.col('uname').is_in(['µg/l', 'µS/cm']))
        .then(pl.col('value') / 1000)
        .otherwise(pl.col('value'))
        .alias('val_mgl'),

        pl.when(pl.col('uname') == 'µg/l')
        .then(pl.lit('mg/l'))
        .when(pl.col('uname') == 'µS/cm')
        .then(pl.lit('mS/cm'))
        .when(pl.col('uname').is_in([
            'mg N/l', 'mg S/l', 'mg S/L', 
            'mg PO4/l', 'mg SO4/l', 'mg P/l',
            'mg P2O5/l',
            ]))
        .then(pl.lit('mg/l'))
        .otherwise(pl.col('uname'))
        .alias('uname_mgl')
    )
)
# %% 4
#macro_list = df_lab_all.filter(pl.col('val_mgl')>1).select(pl.col('cname')).unique()


EC_list = [
    'Geleidbaarheid (25Â°C)'
]
macro_list = [
    'pH', 'Natrium [Na]', 'Kalium [K]', 'Calcium [Ca]', 
    'Magnesium [Mg]', 'IJzer [Fe]', 'Mangaan [Mn]', 
    'Ammonium (als NH4)', 'Fosfaat (als PO4)',
    'Bicarbonaat', 'Chloride', 'Sulfide', 
    'Sulfaat (als SO4)', 
    'Aluminium [Al]', 'Zink [Zn]', 'Koper [Cu]', 'Nikkel [Ni]', 
    'Cadmium [Cd]', 'Arseen [As]', 'Tin [Sn]', 'Silicium [Si]',
    'Temperatuur',
]

others_list = [
    'CZV', 'BZV-5', 'DOC', 'Totaal anorganisch koolstof [TIC]', 
    'Totaal organisch koolstof [TOC]'
]

# %% 5
# Check the number of measurements per sampling point and parameter
# This is to check if there are enough measurements for a time series plot
(df_lab_all.filter(
    pl.col('cname').is_in(macro_list)
).group_by(['measpointname', 'cname'])
 .agg(pl.len())
 .sort(['measpointname','cname'], descending=False) 
 .write_excel('df_lab_macros.xlsx')
)    

# %% 9
def remove_outliers_detrend(
    df: pl.DataFrame,
    date_col: str = 'date',
    value_col: str = 'value',
    deg: int = 1,
    iqr_factor: float = 1.5,
) -> pl.DataFrame:
    """Remove outliers by applying IQR filtering on residuals from a polynomial trend.

    Fits a polynomial of degree `deg` to the time series, computes residuals,
    and drops rows where the residual falls outside `iqr_factor` * IQR.
    Works correctly for data with a monotonic increasing or decreasing trend.

    Parameters
    ----------
    df         : input dataframe, will be sorted by date_col
    date_col   : name of the date column
    value_col  : name of the numeric value column to filter on
    deg        : polynomial degree for trend fit (1 = linear, 2 = quadratic)
    iqr_factor : multiplier for the IQR fence (1.5 = standard, 3.0 = loose)
    """
    df_sorted = df.sort(date_col)
    x = (df_sorted[date_col] - df_sorted[date_col].min()).dt.total_days().to_numpy().astype(float)
    y = df_sorted[value_col].to_numpy()

    coeffs = np.polyfit(x, y, deg=deg)
    residuals = y - np.polyval(coeffs, x)

    q1, q3 = np.percentile(residuals, [25, 75])
    iqr = q3 - q1
    mask = (residuals >= q1 - iqr_factor * iqr) & (residuals <= q3 + iqr_factor * iqr)

    return df_sorted.filter(pl.Series(mask))

# %% 10
# We will remove all non-detects and then outliers.
df_lab_all_clean = (
    df_lab_all
    .filter(pl.col('detectlim') != '<')
)

# Remove outliers for all macros
# We apply per measurement point and parameter, as the trends 
# and variability can differ between them


df_macros_filtered = (
    df_lab_all_clean.filter(pl.col('cname').is_in(macro_list))
    .group_by('cname')
    .map_groups(remove_outliers_detrend)
    .group_by([
        'compartment', 'measpointname', 
        'date', 'cname', 'uname_mgl'])
    .agg(pl.col('val_mgl').mean())
    .sort('date')
)

# There are some samples which have duplicate measurements
# %% 6

# plot the time series for the different parameters and sampling points
plt.close('all')

run_plot = False
if run_plot:
    for param in macro_list:
        df_param = df_macros_filtered.filter(pl.col('cname') == param)
        if df_param.height > 0:
            plt.figure(figsize=(10,6))
            sns.lineplot(
                data=df_param.to_pandas(), 
                x='date', 
                y='val_mgl', 
                hue='measpointname',
                marker='o'
            )
            plt.title(f'Time series of {param}')
            plt.xlabel('Date')
            plt.ylabel('Concentration (mg/L)')
            plt.legend(title='Sampling Point')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()


# %% 8
if run_plot:
    plt.close('all')
    for param in EC_list:
        df_param = df_lab_all.filter(pl.col('cname') == param)
        if df_param.height > 0:
            plt.figure(figsize=(10,6))
            sns.lineplot(
                data=df_param.to_pandas(), 
                x='date', 
                y='val_mgl', 
                hue='measpointname',
                marker='o'
            )
            plt.title(f'Time series of {param}')
            plt.xlabel('Date')
            plt.ylabel('Conductivity (mS/cm)')
            plt.legend(title='Sampling Point')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
# %% 11
# Export the cleaned data to an Excel file for use in assignments
# We will export the data for each the following sampling points to a 
# separate excel file:
# - BoZ.CWZI-inf
 

sampling_points_to_export = [
    'BoZ.CWZI-inf', 'PP-11N', 'PP-11Z', 'PP-12', 'IDS-put 6'
]

for sp in sampling_points_to_export:
    df_export = df_macros_filtered.filter(
        pl.col('measpointname') == sp
        ).sort('date')[
            'compartment', 'measpointname', 'date', 
            'cname', 'val_mgl', 'uname_mgl'
            ]
    df_export.write_excel(f'df_macros_{sp}.xlsx')

# %%
# We now want to analyze the samples with most macro measurements with 
# ORCHESTRA. We first will identify the samples with the most macro measurements, and then export

df_macro_counts = (
    df_macros_filtered.group_by('measpointname','date')
    .agg(pl.count('cname').alias('macro_count'))
    .sort('macro_count', descending=True)
)

df_macro_counts.filter(pl.col('macro_count') >= 10)
# %%
# Check which parameters are measured in the samples with the most macro measurements
df_pars_in_sample = (df_macros_filtered.join(
    df_macro_counts.filter(pl.col('macro_count') >= 30)
    .select(['measpointname', 'date']),
        on=['measpointname', 'date'],
        how='inner')
    .select(['measpointname', 'date', 'cname'])
    .group_by(['measpointname', 'date'])
    .agg(pl.col('cname').unique().alias('parameters'))
    .sort(['measpointname', 'date'])
)
# %%

