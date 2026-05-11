# %%

# For the student assignments we will use pandas 
# for data manipulation and plotting. 
# We will also use seaborn for plotting.

import scipy as sp
import numpy as np
#import pandas as pd
import pandas as pd
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
# import the data set from the excel file.
# We will use the data from the leachate monitoring at PP-11N.

df_leachate = pd.read_excel('data/df_macros_PP-11N.xlsx')

# %% 2
# Check which dates have most parameters measured.
# We will use these parameters as our input for the Orchestra 
# calculation.

# For some dates, less parameters were measured. We can then choose to work 
# with the estimated values, using the time series.

# df_macro_counts = (
#     df_leachate.group_by('measpointname','date')
#     .agg(pl.count('cname').alias('macro_count'))
#     .sort('macro_count', descending=True)
# )

df_par_counts = (
    df_leachate.groupby(['measpointname', 'date'])['cname']
    .count()
    .reset_index(name='macro_count')
    .sort_values('macro_count', ascending=False)
)

df_par_counts
date_with_most_pars = df_par_counts.iloc[0]['date']

# %%
# We use the date with most parameters for our first analysis
sel_idx = df_leachate['date'] == date_with_most_pars

df_work = df_leachate[sel_idx].copy()

# Export df_work to an Excel file so that we can 
# have a quick access to the parameters in it
# for setting up the translation from mg/l to moles/l 
# for the Orchestra input.
# %%
df_work.to_excel('tmp/df_work_PP-11N.xlsx', index=False)

# %%
# Using the content from the file we now create a table
# with the parameters, their values and the conversion to moles/l.
# We will use this table to set up the translation from mg/l to moles/l
# for the Orchestra input.

# Conversion table contaings molar masses for the parameters 
# in the df_work dataframe and the corresponding parameter names
# in the Orchestra input file.
conversion_table = {
    'Sulfaat (als SO4)': [96.06, 'SO4-2.tot'],
    'Sulfide': [32.07, 'S-2.tot'],
    'Natrium [Na]': [22.99, 'Na+.tot'],
    'Nikkel [Ni]': [58.69, 'Ni.tot'],
    'IJzer [Fe]': [55.85, 'Fe.tot'],
    'Zink [Zn]': [65.38, 'Zn.tot'],
    'Magnesium [Mg]': [24.31, 'Mg+2.tot'],
    'Calcium [Ca]': [40.08, 'Ca+2.tot'],
    'Ammonium (als NH4)': [18.04, 'NH4+.tot'],
    'Chloride': [35.45, 'Cl-.tot'],
    'Bicarbonaat': [61.02, 'HCO3-.tot'],
    'Fosfaat (als PO4)': [94.97, 'PO4-3.tot'],
    'Kalium [K]': [39.10, 'K+.tot'],
    'Silicium [Si]': [28.09, 'Si.tot'],
    'Mangaan [Mn]': [54.94, 'Mn.tot'],
    'Arseen [As]': [74.92, 'As.tot'],
}

# We can now use this conversion table 
# to convert the values in the df_work dataframe
# from mg/l to moles/l and to add a new column with Orchestra parameter names.

df_work['val_mol_l'] = df_work.apply(
    lambda row: 
        (row['val_mgl'] * 1e-3) / conversion_table[row['cname']][0] 
        if row['cname'] in conversion_table else row['val_mgl'], axis=1)

df_work['orchestra_param'] = df_work.apply(
    lambda row: 
        conversion_table[row['cname']][1] 
        if row['cname'] in conversion_table else row['cname'], axis=1)


# %%
# Rewrite df_work to excel so we can copy the contents to the Orchestra input file.
df_work.to_excel('tmp/df_work_PP-11N_converted.xlsx', index=False)
# %%
