#!/usr/bin/env python3
# -*- coding: utf-8 -*

#ORCHESTRA
import numpy as np
import pandas as pd
import PyORCHESTRA
def ORCHESTRA_ini(chemistry_file, reaction_file, mDim):
    """initialise ORCHESTRA class"""
    
    nN = mDim.nN

    #import csv file
    df = pd.read_csv(reaction_file).set_index('name')

    #make file ready for further changes
    df_orch = df.drop(['mu_max', 'K_pH', 'pH_opt1', 'pH_opt2', 'kT', 'T_opt', 'limiting_substrate', 'monitoring_species'], axis=1)
    df.loc['Gf'] = df_orch.loc['Gf'].fillna(-999.) #fill all NaN values with -999. in the Gf row for easy selection later on

    #get ORCHESTRA vectors
    IN = np.array(df_orch.filter(like='.tot').columns) #input, all column names with .tot
    IN = np.append(IN, ['porosity', 'saturation', 'wastefraction']) #add porosity, saturation and wastefraction at the end of the list

    OUT = np.array(df_orch.loc[:, df.loc['is_output'] == 'yes'].columns).astype('str') #get columns for output
    OUT_logact = np.char.replace(OUT, '.tot', '.logact') #change .tot to .logact in output array

    #In the out vector, include also share of totals that are in solid and liquid fraction
    OUT_solutionphase = np.char.replace(IN.astype(str), '.tot', '.solution')
    OUT_solidphase = np.char.replace(IN.astype(str), '.tot', '.solid')
    
    OUT_tot = np.concatenate((OUT_logact, OUT_solutionphase, OUT_solidphase))
    #sVecIni_bio = np.array([df_orch.filter(like='.tot').loc['initial']]).astype('float32')#the first row is a list with initial values, use this for check

    p = PyORCHESTRA.ORCHESTRA()
    p.initialise(chemistry_file, nN, IN, OUT_tot)

    return p, IN


