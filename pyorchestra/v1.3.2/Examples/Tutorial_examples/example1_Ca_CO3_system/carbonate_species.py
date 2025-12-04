#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 12:30:36 2022

@author: guidodezeeuw
"""

import numpy as np
import matplotlib.pyplot as plt
import PyORCHESTRA # here, the ORCHESTRA submodule is imported

p = PyORCHESTRA.ORCHESTRA()

InputFile = 'chemistry1.inp'
NoCells = 1 #only 1 cell to have a 0-D system 
InVars = np.array(['Ca+2.tot', 'CO3-2.tot', 'pH', 'porosity', 'saturation'])
OutVars = np.array(['CaCO3.con', 'CO3-2.con', 'HCO3-.con', 'H2CO3.con', 'Ca+2.con',    
		'Calcite[s].min'])

p.initialise(InputFile, NoCells, InVars, OutVars)

IN = np.array([np.ones_like(InVars)]).astype(float)

IN[0][np.where(InVars == 'porosity')] = 1
IN[0][np.where(InVars == 'saturation')] = 1
IN[0][np.where(InVars == 'Ca+2.tot')] = 0.5
IN[0][np.where(InVars == 'CO3-2.to')] = 0.5

pH_list = np.arange(2,12,0.001) # range of pH

# define output lists
CaCO3, CO3, HCO3, H2CO3, Ca, calcite = [], [], [], [], [], []

# loop over every pH
for pH in pH_list:

   # change pH
   IN[0][np.where(InVars == 'pH')] = pH

   # run ORCHESTRA
   OUT = p.set_and_calculate(IN)

   # get output
   CaCO3.append(OUT[0][np.where(OutVars =='CaCO3.con')])
   CO3.append(OUT[0][np.where(OutVars == 'CO3-2.con')])
   HCO3.append(OUT[0][np.where(OutVars == 'HCO3-.con')])
   H2CO3.append(OUT[0][np.where(OutVars == 'H2CO3.con')])
   Ca.append(OUT[0][np.where(OutVars == 'Ca+2.con')])
   calcite. append(OUT[0][np.where(OutVars == 'Calcite[s].min')])


""" PLOTTING RESULTS """
#put all data in a list

#initialise figure
fig, ax = plt.subplots(2,3, figsize=(10,5))

#plotting...
ax[0,0].plot(pH_list, calcite, color='k')
ax[0,1].plot(pH_list, CaCO3, color='k')
ax[0,2].plot(pH_list, Ca, color='k')
ax[1,0].plot(pH_list, CO3, color='k')
ax[1,1].plot(pH_list, HCO3, color='k')
ax[1,2].plot(pH_list, H2CO3, color='k')

#set titles...
ax[0,0].set_title('Calcite')
ax[0,1].set_title(r'$CaCO_3$')
ax[0,2].set_title(r'$Ca^{+2}$')
ax[1,0].set_title(r'$CO_3^{-2}$')
ax[1,1].set_title(r'$HCO_3^-$')
ax[1,2].set_title(r'$H_2CO_3$')

plt.suptitle('Example 1: Results', fontsize=20)

#set labels
for (m,n), subplot in np.ndenumerate(ax):
    subplot.set_xlabel('pH [-]')
ax[0,0].set_ylabel('[mol/L]')
ax[1,0].set_ylabel('[mol/L]')

plt.tight_layout()

plt.savefig('Results.pdf')





