#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 15:55:27 2022

@author: guidodezeeuw
"""

import numpy as np
import matplotlib.pyplot as plt
import PyORCHESTRA # here, the ORCHESTRA submodule is imported

p = PyORCHESTRA.ORCHESTRA()

InputFile = 'chemistry1.inp'
NoCells = 1 #only 1 cell to have a 0-D system 
InVars = np.array(['calcite_mineral.tot', 'Ca+2.tot', 'CO3-2.tot', 'H+.tot', 'porosity', 'saturation'])
OutVars = np.array(['pH'])
p.initialise(InputFile, NoCells, InVars, OutVars)

IN = np.array([np.ones_like(InVars)]).astype(float)

IN[0][np.where(InVars == 'porosity')] = 1
IN[0][np.where(InVars == 'saturation')] = 1
IN[0][np.where(InVars == 'Ca+2.tot')] = 0.5
IN[0][np.where(InVars == 'CO3-2.tot')] = 0.5
IN[0][np.where(InVars == 'H+.tot')] = 0.1

calcite_list = np.arange(0.0,0.5,0.001) # range of calcite_mineral

# define output lists
pH = []

# loop over every calcite
for calcite in calcite_list:
    # change amount of calcite
    IN[0][np.where(InVars == 'calcite_mineral.tot')] = calcite

    # run ORCHESTRA
    OUT = p.set_and_calculate(IN)
    
    #get output
    pH.append(OUT[0])


""" PLOT RESULTS """
plt.plot(calcite_list[::-1],pH, color='k')
plt.title('pH with dissolving calcite', fontsize = 20)
plt.xlabel('calcite concentration [mol/L]')
plt.ylabel('pH [-]')
plt.savefig('result_example2.pdf')