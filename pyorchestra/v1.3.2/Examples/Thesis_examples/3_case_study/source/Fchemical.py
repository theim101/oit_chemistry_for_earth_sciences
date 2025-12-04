#!/usr/bin/env python3
# -*- coding: utf-8 -*

#chemical rates
import numpy as np
from source import Forchestra as Forch
import PyORCHESTRA
from source import Fwater as Fwat

def Flambda_cat(stoich, activities, sBio, T):
    #some constants...
    R=8.314e-3 #gas constant
    beta = np.zeros(len(activities))+1 #vector that helps with matrix transformations
    pos_mon = np.array(stoich.params['monitoring_species']).astype('int')

    #------------------------------------------------------
    # calculate DG0
    #------------------------------------------------------
    D_G0_Cat = np.sum(stoich['Cat']*stoich['Gibbs'], axis=1)
    D_G0_An = np.sum(stoich['An']*stoich['Gibbs'], axis=1)

    #------------------------------------------------------
    # calculate DG1 using logactivities
    #------------------------------------------------------
    logact = np.where(activities!=0, np.log(activities), 0)  
    D_G1_Cat = D_G0_Cat +R*(T+273)*np.sum(stoich['Cat']*logact, axis=1)
    D_G1_An = D_G0_An + R*(T+273)*np.sum(stoich['An']*logact, axis=1)

    #------------------------------------------------------
    # calculate DG_diss = G_diss 
    #------------------------------------------------------    
    DG_dis = np.array(stoich.params['DG_dis'])

    #------------------------------------------------------
    # calculate lambda_cat. 
    # set to 1 for all catabolic reactions that do not partake in metabolic reactions (for D_G1_An = 0)
    #------------------------------------------------------
    lambda_cat = np.array([1.*(D_G1_An ==0.) + (D_G1_An+DG_dis)/D_G1_Cat]).T  * beta
    
    return lambda_cat    

def Fnewstoich(stoich, activities, sBio, T):
    #some constants...
    beta = np.zeros(len(activities))+1 #vector that helps with matrix transformations

    #------------------------------------------------------
    # calculate final stoichiometry (Met = lambda_cat * Cat + An)
    #------------------------------------------------------    
    lambda_cat = Flambda_cat(stoich, activities, sBio, T)
    M = abs(lambda_cat)*stoich['Cat'] + stoich['An']

    #------------------------------------------------------
    # normalize to component that is monitored
    #------------------------------------------------------
    NR = np.arange(len(stoich['Cat'])) #number of reactions
    
    pos_mon = np.array(stoich.params['monitoring_species']).astype('int') - 3 #position of monitoring substrate
    norm = np.array([M[NR,pos_mon]]).T * beta #normalized to monitoring substrate
    M_normalized = M/abs(norm)    #normalized metabolic reactions
    return M_normalized

def Finhibitions(sBio, activities, stoich, pH, T, NH4_sorbed):
    #inhibition by main substrate limitation
    lim_indices = np.array(stoich.params['limiting_substrate']).astype('int') #indices in matrix of limiting substrates
    f_lim_main = sBio[:][lim_indices] / (np.array([stoich.params['K_lim_main']]).T + sBio[:][lim_indices])

    #inhibition by substrate limitation
    f_lim_NH4 = np.array([activities[6]/(stoich.params['K_lim_NH4']+activities[6])]).T
    f_lim_NO3 = np.array([activities[7]/(stoich.params['K_lim_NO3']+activities[7])]).T
    f_lim_O2 = np.array([activities[8]/(stoich.params['K_lim_O2']+activities[8])]).T 

    #inhibitions by temperature and pH: reichel (2007):
    f_pH = np.array([stoich.params['K_pH']/((stoich.params['K_pH'] + (10**pH)/(10**stoich.params['pH_opt1']) +(10**stoich.params['pH_opt2'])/(10**pH)) -2)]).T
    f_T = np.array([np.exp(-(stoich.params['kT']*(21-stoich.params['T_opt']))**2)]).T

    #inhibition by presence of biomass
    som_X = (sBio[7,0]+sBio[6,0]+sBio[5,0]+sBio[8,0])
    f_X = np.array([(sBio[7,0]+sBio[6,0]+sBio[5,0]+sBio[8,0])/(stoich.params['K_X']+(sBio[6,0]+sBio[5,0]+sBio[7,0]+sBio[8,0]))]).T

    #inhibition by toxicity
    f_tox_O2 = np.array([1-   activities[8] /(stoich.params['K_tox_O2']+activities[8])]).T
    f_tox_NH4 = np.array([1-activities[6]/(stoich.params['K_tox_NH4']+activities[6])]).T

    #total inhibitions
    f_tot = f_lim_main * f_lim_NH4 * f_lim_NO3 * f_lim_O2 * f_pH * f_T * f_X * f_tox_O2 * f_tox_NH4
    return f_tot

def Fchemrates(t, sBio, sGas, pH, O2gas_activity, NH4_sorbed, activities, sPar, bPar, stoich):
    """calculate rate for chemical processes"""
    #some constants...
    T = 21 #degrees celcius
    #------------------------------------------------------
    # calculate new stoichiometry based on molar activities
    #------------------------------------------------------
    M_normalized = Fnewstoich(stoich,activities, sBio, T)

    #------------------------------------------------------
    # calculate inhibitions
    #------------------------------------------------------
    f_tot = Finhibitions(sBio, activities, stoich, pH, T, NH4_sorbed)

    #------------------------------------------------------
    # calculate rates
    #------------------------------------------------------
    R = np.array([stoich.params['mu_max']]).T * f_tot

    #------------------------------------------------------
    # SPECIAL CASES
    #------------------------------------------------------
    switch = bPar.switch(t) #see Fparameters for definition
    R[9] = switch* np.array(stoich.params['mu_max'])[9] * (0.2 - O2gas_activity)/0.2 #SPECIAL CASE WHERE THE OXYGEN IS ADDED (is 9th reaction in input file)!!!
    R[0] = R[0] * sBio[3,0]/(2+sBio[3,0]) #SPECIAL CASE WHERE WASTE GETS HARDER TO DEGRADE OVER TIME (EASILY, MODERATELY, HARDLY DEGRADABLE)
    #------------------------------------------------------
    # calculate change (=rate*stoichiometry)
    #------------------------------------------------------
    
    nn, mm = R.shape
    if mm > 1:
        R = np.array([R[:,0]]).T

    M_normalized = M_normalized*R #for every individual species 
    M_sum = M_normalized.sum(axis=0) #sum of reactions
    
    #------------------------------------------------------
    # finalize rate vector
    # HERE IS A PIECE OF HARDCODING, NUMBER OF MONITORING SPECIES IS UNKOWN IN M_NORM. 
    # NEED TO KNOW AMOUNT OF TOTAL ELEMENTS (E.G. C.tot/H.tot/N.tot) TO SPECIFY LENGTH CORRECTLY
    #------------------------------------------------------
    R_bio = np.zeros_like(sBio)
    R_bio[3:-3] = np.array([M_sum[:10]]).T
    
    R_gas = np.zeros_like(sGas)
    R_gas[:] = np.array([M_sum[10:12]]).T
    return R_bio, R_gas

def FCR(t, sBio, sGas, p, sPar, bPar, stoich):
    print(f'{t/365.25} years') #Print time to monitor
    """function that returns changes in composition using ORCHESTRA"""

    ################################################################################################
    #-------------------------    CHEMICAL CHANGES ------------------------------------------------#
    ################################################################################################
    #------------------------------------------------------
    # calculate equilibrium with ORCHESTRA
    #------------------------------------------------------
    equilibrium = p.set_and_calculate(sBio.T)#equilibrium = OutVars
    #------------------------------------------------------
    # get values of interest (HARDCODED)
    #------------------------------------------------------
    pH = equilibrium[0][16]
    O2gas_activity = 10**(equilibrium[0][15]) #oxygen gas activity (10**O2[g].logact)
    NH4_sorbed = equilibrium[0][17] * sBio[-3,0]*sBio[-2,0]/((1-(sBio[-3,0]*sBio[-1,0]))) #porosity * saturation/(1-porosity*wastefraction) 
    activities = np.array(equilibrium[0][:15])

    activities = 10**activities #activities by ORCHESTRA are given in log10, get non-logarithmic values.

    #------------------------------------------------------
    # calculate reaction change using pH and activities
    #------------------------------------------------------
    R_bio, R_gas = Fchemrates(t, sBio, sGas, pH, O2gas_activity, NH4_sorbed, activities, sPar, bPar, stoich) 


    ###############################################################################################
    #-------------------------    TRANSPORT CHANGES ------------------------------------------------#
    ################################################################################################


    ###############################################################################################
    #-------------------------    SYSTEM CHANGES ------------------------------------------------#
    ################################################################################################
    #porosity (dependent on waste change)
    waste_area = (1-sBio[-3,0])*sBio[-1,0] #current waste area =  (1-porosity) * wastefraction
    d_waste_area = R_bio[3,0] / sBio[3,0] * waste_area # = d_waste / waste * waste_area
    d_porosity = -d_waste_area 

    #wastefraction
    d_wastefraction = -(sBio[-1,0] - ((waste_area+d_waste_area)/((1-sBio[-3,0])-d_porosity)))

    #saturation
    liquid_tot = sBio[-3,0] * sBio[-2,0] #porosity * saturation
    saturation_new = liquid_tot/(sBio[-3,0] + d_porosity)
    d_saturation = saturation_new - sBio[-2,0]

    ################################################################################################
    #----------------------------    TOTAL CHANGES ------------------------------------------------#
    ################################################################################################
    #add everything together!
    d_totals = 0*sBio[:-3,0] #change of totals by transport
    d_totals = np.append(d_totals, [d_porosity,d_saturation,d_wastefraction]) #include porosity/saturation and wastefraction
    R_bio = R_bio + (d_totals*np.ones_like(R_bio).T).T #combine with chemical changes

    return R_bio, R_gas
