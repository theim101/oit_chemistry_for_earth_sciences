#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 1 11:50:00 2024

@author: theimovara

Example script for using PyORCHESTRA
CASE: Ca CO3 speciation in 1 liter of water in equilibrium with 1 liter
of gas. Background gas is 1 atm Ar with a limited solubility.

Python script iterates over pH range

"""
# %%
import numpy as np
import matplotlib.pyplot as plt
import PyORCHESTRA # here, the ORCHESTRA submodule is imported
import pandas as pd
import seaborn as sns

#%matplotlib qt5
sns.set()

p = PyORCHESTRA.ORCHESTRA()

# %%
InputFile = 'chemistry1.inp'
NoCells = 1 #only 1 cell to have a 0-D system 

InVars = np.array(['H.tot', 'CO3-2.tot', 'Ca+2.tot','Na.tot', 
        'Ar[g].logact', 'gasvolume','watervolume'])

OutVars = np.array(['pH', 'H.tot', 'H+.con', 'CO2[g].logact', 
        'CO3-2.tot', 'H2CO3.con', 'HCO3-.con', 'CO3-2.con', 
        'Ca+2.con', 'CaCO3.con', 'Calcite[s].tot', 
        'Na+.con', 'OH-.con', 'pressure'])

p.initialise(InputFile, NoCells, InVars, OutVars)

# %%
# Initialize problem
IN = np.array([np.ones_like(InVars)]).astype(float)

IN[0][np.where(InVars == 'Ca+2.tot')] = 0.1 # moles
IN[0][np.where(InVars == 'Na+.tot')] = 0.1 # moles
IN[0][np.where(InVars == 'CO3-2.tot')] = 0.1 # moles
IN[0][np.where(InVars == 'H.tot')] = 1e-7 # background pressure Ar = 1 atm
IN[0][np.where(InVars == 'gasvolume')] = 1 # liter
IN[0][np.where(InVars == 'watervolume')] = 1 # liter
IN[0][np.where(InVars == 'Ar[g].logact')] = 0 # liter
IN[0][np.where(InVars == 'CO2[g].logact')] = 0 # liter

# run orchestra with default settings
# OUT = p.set_and_calculate(IN)

# Define range for pH titration
# because of instablity solution for low pH, run problem from high to low pH
# this is a trial and error approach
CO3_list = np.logspace(-3, 0, 100) # range of pH

#Initialize output
all_Res = np.zeros([len(CO3_list),len(OutVars)])

# loop over every pH
for CO3_tot in CO3_list:
    # change pH in InVars
    IN[0][np.where(InVars == 'CO3-2.tot')] = CO3_tot

    # run ORCHESTRA
    OUT = p.set_and_calculate(IN)

    all_Res[CO3_list == CO3_tot] = OUT[0]

    # Create a dataframe from all_Res
    Orch_Res = pd.DataFrame(all_Res,columns=OutVars)

# %%
# """ PLOTTING RESULTS """

# #initialise figure
fig, ax = plt.subplots(2,2, figsize=(10,5))

# #plotting...
Orch_Res.plot(x='pH',y='H2CO3.con',style='r+-',ax=ax[0,0])
Orch_Res.plot(x='pH',y='HCO3-.con',style='g+-',ax=ax[0,0])
Orch_Res.plot(x='pH',y='CO3-2.con',style='y+-',ax=ax[0,0])
Orch_Res.plot(x='pH',y='CO2[g].logact',style='+-',ax=ax[1,0])
Orch_Res.plot(x='pH',y='Ca+2.con',style='r+-',ax=ax[0,1])
Orch_Res.plot(x='pH',y='Calcite[s].tot',style='g+-',ax=ax[0,1])
Orch_Res.plot(x='pH',y='pressure',style='+-',ax=ax[1,1])

# %%
# #initialise figure
fig1, ax1 = plt.subplots(2,2, figsize=(10,5))

# #plotting...
Orch_Res.plot(x='CO3-2.tot',y='H2CO3.con',style='r+-',ax=ax1[0,0])
Orch_Res.plot(x='CO3-2.tot',y='HCO3-.con',style='g+-',ax=ax1[0,0])
Orch_Res.plot(x='CO3-2.tot',y='CO3-2.con',style='y+-',ax=ax1[0,0])
Orch_Res.plot(x='CO3-2.tot',y='CO2[g].logact',style='+-',ax=ax1[1,0])
Orch_Res.plot(x='CO3-2.tot',y='Ca+2.con',style='r+-',ax=ax1[0,1])
Orch_Res.plot(x='CO3-2.tot',y='Calcite[s].tot',style='g+-',ax=ax1[0,1])
Orch_Res.plot(x='CO3-2.tot',y='pH',style='+-',ax=ax1[1,1])

# %%
import pygwalker as pyg

walker = pyg.walk(Orch_Res)