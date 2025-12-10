#!/usr/bin/env python3
# -*- coding: utf-8 -*

#parameters and definitions
import pandas as pd
import numpy as np
import math
def parameters(nIN, height, reaction_file):
    """
    initialise function that returns dictionaries with data
    """
    
    zIN = np.linspace(-height,0,num=nIN).reshape(nIN,1)
    zN = np.zeros(nIN-1).reshape(nIN-1,1)
    zN[1:nIN - 2, 0] = (zIN[1:nIN - 2, 0] + zIN[2:nIN - 1, 0]) / 2
    zN[nIN - 2, 0] = zIN[nIN - 1]
    nN = np.shape(zN)[0]
    
    def optional_function1():
        """do something"""
        return """something"""
    
    def optional_function2():
        """do something"""
        return """something"""
    
    
    mDim = {'zN' : zN,
            'zIN' : zIN,
            'nN' : nN,
            'nIN' : nIN
            }


    sPar = {
        'mC' : 12,
        'mH' : 1.008,
        'mO' : 16,
        'mN' : 14.007,
        'solid_Ini' : 0.75, #initial solid fraction
        'waste_fraction_Ini' : 0.05, #initial waste fraction of the solid
        'waste_Ini' : 0.13, #initial mol of waste
        }
    
    #set a cyclic on/off switch that opens or closes the system
    def system_lid(t):
        cycle = 0 + 1*math.sin((math.pi*2/(365.25*3) * t/2)) +0.97
        switch = 1*(cycle<0) + 0
        return switch

    bPar ={
        'switch' : system_lid,
        }
    mDim = pd.Series(mDim)
    sPar = pd.Series(sPar)
    bPar = pd.Series(bPar)

    return mDim, sPar, bPar 


def waste_fermentation(comp_waste, Cat):
    #function to define stoichiometry of waste fermentation depending on compostion
    
    column_names = Cat.columns
    df_fermentation = pd.DataFrame(columns=column_names)
    row = np.empty(len(column_names))

    #first, add the electron giving reaction
    df_fermentation.loc[df_fermentation.shape[0]] = row
    #the fermentation reaction of waste can be mathematically described calculating for the following values:
    #(A)waste   + (B)H2O     --> (C)CH3COO-   +  (D)NH4+     +  (E)H+
    #normalized to waste
    df_fermentation['waste.tot'].iloc[0] = -1 
    df_fermentation['acetate.tot'].iloc[0] = 0.5*comp_waste[0]
    df_fermentation['NH4+.tot'].iloc[0] = 1*comp_waste[3]
    df_fermentation['H2O.logact'].iloc[0] = -(df_fermentation['waste.tot'].iloc[0]*comp_waste[2] +  df_fermentation['acetate.tot'].iloc[0] * 2)
    df_fermentation['H+.logact'].iloc[0]  = abs(df_fermentation['waste.tot'].iloc[0] * comp_waste[1]) + abs(df_fermentation['H2O.logact'].iloc[0]*2) - df_fermentation['acetate.tot'].iloc[0]*3 -df_fermentation['NH4+.tot'].iloc[0]*4
    
    #get electron deficit
    e_don = -1*df_fermentation['acetate.tot'].iloc[0] + 1*df_fermentation['NH4+.tot'].iloc[0] + 1*df_fermentation['H+.logact'].iloc[0] 
    
    #now for the electorn accepting reaction where we take acetate as acceptor
    df_fermentation.loc[df_fermentation.shape[0]] = row
    df_fermentation['acetate.tot'].iloc[1] = 1
    df_fermentation['H2O.logact'].iloc[1] = 4 
    df_fermentation['HCO3-.logact'].iloc[1] = -2 
    df_fermentation['H+.logact'].iloc[1] = -9

    e_acc = 8 #the accepting reaction is 8
    factor = e_don/e_acc #calculate ratio between donor and acceptor reaction
    df_fermentation.iloc[1] =df_fermentation.iloc[1] * factor #multiply the accepting reaction by factor
    
    #get sum and normalize again to waste
    df_fermentation.loc[df_fermentation.shape[0]] = row 
    df_fermentation.iloc[2] = df_fermentation.iloc[0] + df_fermentation.iloc[1]

    #replace empty values with NaN
    df_fermentation.iloc[2][abs(df_fermentation.iloc[2]) < 1e-100] = np.nan
    return df_fermentation 

def read_input_file(reaction_file, comp_waste):
    df = pd.read_csv(reaction_file).set_index('name') #get full dataframe and set name to index

    #--------------------------
    # get dataframe with all the parameters
    #--------------------------
    df_parameters = df[['mu_max', 'K_pH', 'pH_opt1', 'pH_opt2', 'kT', 'T_opt', 'K_tox_O2', 'K_lim_O2', 'K_tox_NH4', 'K_lim_NH4' , 'K_lim_NO3','limiting_substrate', 'K_X', 'K_lim_main', 'DG_dis', 'monitoring_species']] #get index with all parameters
    df_parameters = df_parameters[df_parameters.index.str.contains('C')] #select only catabolic reactions

    #--------------------------
    # get dataframe with stoichiometry
    #--------------------------
    df_reactions = df.drop(['mu_max', 'K_pH', 'pH_opt1', 'pH_opt2', 'kT', 'T_opt', 'limiting_substrate', 'K_X', 'K_lim_main', 'monitoring_species'], axis=1)
    df_reactions.loc['Gf'] = df_reactions.loc['Gf'].fillna(-999.) #fill all NaN values with -999. in the Gf row for easy selection later on
    df_reactions.loc['Molar_mass'] = df_reactions.loc['Molar_mass'].fillna(-999.)
    
    #get new fermentation reaction based on waste composition
    df_fermentation = waste_fermentation(comp_waste, df_reactions)
    df_reactions.loc['C1'] = df_fermentation.iloc[2]
    #---------------------------
    # get anabolic and catabolic matrices
    #---------------------------
    molar_mass = np.array(df_reactions.loc['Molar_mass', df_reactions.loc['Molar_mass'] != -999])
    df_reactions = df_reactions.loc[:, df_reactions.loc['Gf'] != -999]
    Gibbsf = np.array(df_reactions.loc['Gf']) #get gibbs free energy vector
    df_catabolic = df_reactions[df_reactions.index.str.contains('C')]
    df_anabolic_or = df_reactions[df_reactions.index.str.contains('A')]
    df_anabolic = pd.DataFrame(0.0, columns=df_catabolic.columns, index=df_catabolic.index) #before we fill in anabolic dataframe, lets make sure it has the same size as the catabolic dataframe

    #---------------------------
    # loop over the index of anabolic functions to determine its position
    # in the final catabolic matrix (index is in name, e.g. A2 is the second reaction)
    #---------------------------
    for index in df.index:  #loop over all indices in original dataframe
        if 'A' in index:    #look for indices containing A (=anabolic)
            number = int(index[1:])  #find the pair number of the anabolic function
            df_anabolic.iloc[number-1] = df_anabolic_or.loc[index]
    
    #---------------------------
    # get index of limiting substrate of .tot variables
    #---------------------------
    tots = np.array(df.filter(like='.tot').columns) 

    for index in df_parameters.index:
        #get the index of the limiting substrate
        limit_substrate = df_parameters['limiting_substrate'].loc[index]
        position_lim = np.where(tots == limit_substrate)
        df_parameters['limiting_substrate'].loc[index] = position_lim[0]
        
        moni_substrate = df_parameters['monitoring_species'].loc[index]
        position_mon = np.where(tots == moni_substrate)
        df_parameters['monitoring_species'].loc[index] = position_mon[0]

    
    #---------------------------
    # set values to floats
    #---------------------------
    Cat = np.array(df_catabolic).astype('float')
    An = np.array(df_anabolic).astype('float')
    #set nan values to 0.
    Cat[np.isnan(Cat)] = 0.
    An[np.isnan(An)] = 0.
    
    
    #---------------------------
    # FINAL: make dict
    #---------------------------
    stoich = {'Cat' : Cat,
              'An' : An,
              'Gibbs' : Gibbsf.astype('float'),
              'params' : df_parameters,
              'molar_mass' : molar_mass.astype('float'),
              'tots' : tots
    }
    stoich = pd.Series(stoich)
    return stoich

