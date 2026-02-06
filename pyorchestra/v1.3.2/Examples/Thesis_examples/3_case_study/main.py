

"""import modules"""
#standard packages
import numpy as np
import matplotlib.pyplot as plt
import sys
import matplotlib
import pandas as pd
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import ScalarFormatter
#ORCHESTRA PACKAGE
import PyORCHESTRA

#personal packages
from source import Fsolver as Fsol
from source import Forchestra as Forch
from source import Fparameters as Fparam

plot = 'yes' #a quick switch to run the solver (set to 'yes'). if no, script will stop after initialisation
"""
###########MAIN SCRIPT#############
"""
# =============================================================================
# system description
# =============================================================================
volume = 1*1e-3 #m^3
porosity = 0.25 #[-]
saturation = 0.8 #[-]
organic_waste_fraction =0.30# 0.3 #[-]
waste_density_dry = 230 #kg/m^3

#some mass calculations...
pure_waste_density = 230/(1-porosity) #kg/m3
total_organic_waste = volume*(1-porosity)*pure_waste_density*organic_waste_fraction #kg

height = 1 #[cell unit]
nIN = 2 #number of cell boundaries. 2 for a 0D system

#path of input files
input_file = "chemistry.inp" #ORCHESTRA input file
reaction_file = "reactions.csv" #stoichiometry input files

##############################################################
#    CHANGE HERE WASTE COMPOSITION !!
##############################################################
#composition of waste [C, H, O, N]
comp_waste = np.array([1, 1.72, 0.5, 0.03125])

comp_waste = comp_waste/comp_waste[0] #normalized to C (first index)
newline = '@composition(waste, ' + str(comp_waste[0]) + ', CO3-2, ' + str(comp_waste[1] - 4*comp_waste[3]) + ', H, ' + str(comp_waste[2] - 3*comp_waste[0]) + ', O)\n'
comp_waste_new = np.array([comp_waste[0], comp_waste[1]-4*comp_waste[3], comp_waste[2]-3*comp_waste[0], comp_waste[3]])
#===================================================================
#change waste composition in chemistry file:
with open(input_file) as f:
    data = f.readlines()
    line_number = 0
    for line in data:
        line_number +=1
        if '@composition(waste' in line:
            data[line_number-1] = newline  

#and save the file again with the new composition
with open(input_file, 'w') as file:
    file.writelines( data )

#==================================================================
#calculate amount of moles
molar_mass_waste = 12*comp_waste[0] + 1.008*comp_waste[1] + 16*comp_waste[2] + 14*comp_waste[3] #g/mol
mol_waste = total_organic_waste *1000 /molar_mass_waste
mol_components_waste = comp_waste*mol_waste 

# =============================================================================
# 2. get parameter dictionaries
# =============================================================================
mDim, sPar, bPar = Fparam.parameters(nIN, height, reaction_file) #model dimensions, parameters, boundary conditions
stoich = Fparam.read_input_file(reaction_file, comp_waste) #read data from input file

# =============================================================================
# 4. initialise ORCHESTRA 
# =============================================================================
p, IN = Forch.ORCHESTRA_ini(input_file, reaction_file, mDim) #containing initialised 'p'-object for ORCHESTRA calculations + IN array with input variable names

# =============================================================================
# 3. initial conditions
# =============================================================================
tOut = np.linspace(0, 365.25*70, 3000) #time range (start, end, how many saved points)

#gas
CO2_Ini = 0 #mol (no gas has been produced before)
CH4_Ini = 0 #mol (no gas has been produced before)
sVecIni_gas = np.array([np.array([CO2_Ini, CH4_Ini])]).astype('float32')

#orchestra totals
IN[np.where(IN == 'CO3-2.tot')]  = 0.27+ comp_waste_new[0]*total_organic_waste*1000/molar_mass_waste 
IN[np.where(IN == 'H.tot')]  = 0.27 + comp_waste_new[1]*total_organic_waste*1000/molar_mass_waste 
IN[np.where(IN == 'NH4+.tot')]  = 0.0
IN[np.where(IN == 'NO3-.tot')] = 1.0e-9 #
IN[np.where(IN == 'Ca+2.tot')]  = 0.47 #2
IN[np.where(IN == 'N2.tot')]  = 1e-9 #2
IN[np.where(IN == 'waste.tot')]  =  total_organic_waste * 1000/molar_mass_waste #moles waste (in ORCHESTRA = mol/L)
IN[np.where(IN == 'acetate.tot')]  = 1.0e-9 # 1.0e-7 
IN[np.where(IN == 'methanogens.tot')]  = 0.01 # 0.01 
IN[np.where(IN == 'oxidizers.tot')]  = 0.01 # 0.01 
IN[np.where(IN == 'nitrifiers.tot')]  = 0.01 # 0.01 
IN[np.where(IN == 'denitrifiers.tot')]  = 0.01 
IN[np.where(IN == 'O2.tot')] = 0.0051
IN[np.where(IN == 'porosity')]  =0.25
IN[np.where(IN == 'saturation')]  =0.9
IN[np.where(IN == 'wastefraction')]  = organic_waste_fraction 

sVecIni_bio = np.array([IN]).astype('float32') #get initial value)

#check if initial configuration is okay (if not, ORCHESTRA will raise an error)
OUT_first_test = p.set_and_calculate(sVecIni_bio) #check if ORCHESTRA works

#combine initial vectors (gas and orchestra tots)
sVecIni = np.concatenate((sVecIni_bio, sVecIni_gas), axis=1) 

if plot == 'yes':
    # =============================================================================
    # 4. start solving!
    # =============================================================================
    int_result =Fsol.solver(tOut, sVecIni, p, sPar, mDim, bPar, stoich) #run ODE solver
    
    # =============================================================================
    # 5. plot results
    # =============================================================================   
    CO3 = int_result.y[mDim.nN*0:mDim.nN*1]
    H = int_result.y[mDim.nN*1:mDim.nN*2]
    Ca = int_result.y[mDim.nN*2:mDim.nN*3]
    Waste1 = int_result.y[mDim.nN*3:mDim.nN*4]
    acetate = int_result.y[mDim.nN*4:mDim.nN*5]
    methanogens = int_result.y[mDim.nN*5:mDim.nN*6]
    oxidizers = int_result.y[mDim.nN*6:mDim.nN*7]
    nitrifiers = int_result.y[mDim.nN*7:mDim.nN*8]
    denitrifiers = int_result.y[mDim.nN*8:mDim.nN*9]
    NH4 = int_result.y[mDim.nN*9:mDim.nN*10]
    NO3 = int_result.y[mDim.nN*10:mDim.nN*11]
    Oxygen = int_result.y[mDim.nN*11:mDim.nN*12]
    N2 = int_result.y[mDim.nN*12:mDim.nN*13]
    porosity = int_result.y[mDim.nN*13:mDim.nN*14]
    saturation = int_result.y[mDim.nN*14:mDim.nN*15]
    wastefraction = int_result.y[mDim.nN*15:mDim.nN*16]
    CO2 = int_result.y[mDim.nN*16:mDim.nN*17]
    CH4 = int_result.y[mDim.nN*17:mDim.nN*18]

    #get remaining parameters by calculating equilibrium for given solutions
    p, IN = Forch.ORCHESTRA_ini(input_file, reaction_file, mDim)

    pH = []
    O_act = []
    O2_act = []
    ammonium_aq = []
    ammonium_ad = []
    nitrate_aq = []
    activities = []
    f_main_inhs = []
    f_pH_inhs = []
    f_NH4_inhs = []
    f_X_inhs = []
    f_NH4_tox_inhs = []
    f_O2_tox_inhs = []
    f_O2_inhs = []
    f_NO3_inhs = []
    for sBio in int_result.y[mDim.nN*0:mDim.nN*16].T:
        IN = np.array([sBio])
        IN = np.where(IN < 0, 1e-15, sBio)
        
        OUT = p.set_and_calculate(IN)
        pH.append(OUT[0][16])
        O_act.append(10**OUT[0][15])
        O2_act.append(10**OUT[0][8])
        ammonium_aq.append(10**OUT[0][6])
        nitrate_aq.append(10**OUT[0][7])
        ammonium_ad.append(OUT[0][17] * IN[0,-3]*IN[0,-2]/((1-(IN[0,-3]*IN[0,-1]))))

        #calculate inhibitions
        lim_indices = np.array(stoich.params['limiting_substrate']).astype('int') #indices in matrix of limiting substrates
        f_main_inh = sBio[lim_indices] / (np.array(stoich.params['K_lim_main']) + sBio[lim_indices])
        f_pH_inh = stoich.params['K_pH']/((stoich.params['K_pH'] + (10**OUT[0][16])/(10**stoich.params['pH_opt1']) +(10**stoich.params['pH_opt2'])/(10**OUT[0][16])) -2)
        f_NH4_inh = 10**OUT[0][6]/(stoich.params['K_lim_NH4']+10**OUT[0][6])
        f_X_inh = (sBio[7]+sBio[6]+sBio[5]+sBio[8])/(stoich.params['K_X']+(sBio[6]+sBio[5]+sBio[7]+sBio[8]))
        f_NH4_tox_inh = 1-10**OUT[0][6]/(stoich.params['K_tox_NH4']+10**OUT[0][6])
        f_O2_tox_inh = 1-   10**OUT[0][8] /(stoich.params['K_tox_O2']+10**OUT[0][8])
        f_O2_inh = 10**OUT[0][8]/(stoich.params['K_lim_O2']+10**OUT[0][8])
        f_NO3_inh = 10**OUT[0][7]/(stoich.params['K_lim_NO3']+10**OUT[0][7])

        f_main_inhs.append(f_main_inh)
        f_pH_inhs.append(f_pH_inh)
        f_NH4_inhs.append(f_NH4_inh)
        f_X_inhs.append(f_X_inh)
        f_NH4_tox_inhs.append(f_NH4_tox_inh)
        f_O2_tox_inhs.append(f_O2_tox_inh)
        f_O2_inhs.append(f_O2_inh)
        f_NO3_inhs.append(f_NO3_inh)
    f_main_inhs = np.array(f_main_inhs)
    f_pH_inhs = np.array(f_pH_inhs)
    f_NH4_inhs = np.array(f_NH4_inhs)
    f_X_inhs = np.array(f_X_inhs)
    f_NH4_tox_inhs = np.array(f_NH4_tox_inhs)
    f_O2_tox_inhs = np.array(f_O2_tox_inhs)
    f_O2_inhs = np.array(f_O2_inhs)
    f_NO3_inhs = np.array(f_NO3_inhs)

    ### PLOT 1 - ANAEROBIC GROWTH ###
 
    ### PLOT 1 - COMPONENTS ###
    fig, ax = plt.subplots(4,2, figsize=(10,7))
    fig.suptitle('Model results for the final case study', fontsize=20)
    #set background for first three plots
    cmap = plt.cm.cool 
    norm = matplotlib.colors.Normalize(vmin=min(O2_act), vmax=max(O2_act))
    for ii in range(len(tOut)-1):
        print(f'plotting... please wait... {ii/(len(tOut)-1) * 100} %')
        for jj in range(4):
            for kk in range(2):
                ax[jj,kk].fill_between([tOut[ii]/365.25, tOut[ii+1]/365.25], -0.1,10, color=cmap(norm(O2_act[ii])),zorder=1, lw=0)
    
    ax[0,0].plot(tOut/365.25, Waste1.T, color='k',zorder=2)
    ax[0,0].set_title('$\\bf{SOM}$')
    ax[0,0].set_ylabel('[mol]')
    ax[1,0].plot(tOut/365.25, acetate.T, color='k')
    ax[1,0].set_title('$\\bf{acetate}$')
    ax[1,0].set_ylabel('[mol/L]')
    ax[2,0].plot(tOut/365.25, methanogens.T, color='k', label='$X_{meth}$')
    ax[2,0].plot(tOut/365.25, oxidizers.T, color='r', label = '$X_{ox}$')
    ax[2,0].plot(tOut/365.25, nitrifiers.T, color='k', ls='--', label='$X_{nitr}$')
    ax[2,0].plot(tOut/365.25, denitrifiers.T, color='k', ls='-.', label='$X_{denitr}$')    
    ax[2,0].set_title('$\\bf{biomass}$')
    ax[2,0].set_ylabel('[mol/L]')
    ax[2,0].legend(loc='upper right', fontsize='small', ncol=4)
    ax[3,0].plot(tOut/365.25, pH, color='k')
    ax[3,0].set_title('$\\bf{pH}$')
    ax[3,0].set_ylabel('[-]')
    ax[0,1].plot(tOut/365.25, ammonium_aq, color='k', label='$NH_4^+$')
    ax[0,1].plot(tOut/365.25, np.ones_like(ammonium_aq), color='red', label='$NO_3^-$')
    nitrate_plot = ax[0,1].twinx()
    nitrate_plot.plot(tOut/365.25, nitrate_aq, color='r')
    ax[0,1].set_title('$\\bf{NH_{4,aq}^+}$ and $\\bf{NO_3^-}$')
    ax[0,1].set_ylabel('[mol/L]')
    ax[0,1].legend(loc=('upper right'), fontsize='small')
    ax[1,1].plot(tOut/365.25, O2_act, color='k')
    ax[1,1].set_title('$\\bf{O_2^{aq}}$')
    ax[1,1].set_ylabel('[mol/L]')
    ax[2,1].plot(tOut/365.25, ammonium_ad, color='k')
    ax[2,1].set_title('$\\bf{NH_{4,ad}^+}$')
    ax[2,1].set_ylabel('[mol/L]')
    #----
    ax[3,1].plot(tOut/365.25, CH4.T, color='k', label='$CH_4$')
    ax[3,1].plot(tOut/365.25, np.ones_like(ammonium_aq)*10, color='red', label='$CO_2$')
    CO2_plot = ax[3,1].twinx()
    CO2_plot.plot(tOut/365.25, CO2.T, color='r')
    ax[3,1].set_title('$\\bf{CH_4}$ and $\\bf{CO_2}$')
    ax[3,1].set_ylabel('[mol/L]')
    ax[3,1].legend(loc=('upper right'), fontsize='small')
    
    #y limits:
    ax[0,0].set_ylim(min(Waste1.T)-0.05*np.mean(Waste1), max(Waste1.T)+0.05*np.mean(Waste1.T))
    ax[1,0].set_ylim(0, max(acetate.T)+0.1*np.mean(acetate.T))
    ax[2,0].set_ylim(0.0,max(denitrifiers.T)+0.1*max(denitrifiers.T))
    ax[3,0].set_ylim(min(pH)-0.05*np.mean(pH), max(pH)+0.05*np.mean(pH))
    ax[0,1].set_ylim(0, max(ammonium_aq)+0.5*np.mean(ammonium_aq))
    nitrate_plot.set_ylim(0, max(nitrate_aq)+0.5*np.mean(nitrate_aq))
    ax[1,1].set_ylim(0, max(O2_act)+0.5*np.mean(O2_act))
    ax[2,1].set_ylim(0, max(ammonium_ad)+0.05*np.mean(ammonium_ad))
    ax[3,1].set_ylim(0, max(CO2.T) +0.05*np.mean(CO2))   
    CO2_plot.set_ylim(0, max(CO2.T) +0.05*np.mean(CO2)) 
    class ScalarFormatterClass(ScalarFormatter):
        def _set_format(self):
            self.format = "%1.2f"
    yScalarFormatter = ScalarFormatterClass(useMathText=True)
    yScalarFormatter.set_powerlimits((0,0))
    for ii in range(4):
        for jj in range(2):
            ax[ii,jj].set_xlim(0,tOut[-1]/365.25)
            ax[ii,jj].yaxis.set_major_formatter(yScalarFormatter)
    nitrate_plot.yaxis.set_major_formatter(yScalarFormatter)
    ax[3,1].set_xlabel('time (year)')
    ax[3,0].set_xlabel('time (year)')

    plt.tight_layout()
    plt.savefig('components_finals.pdf')
    plt.show()

    #plot inhibitions
    fig, ax = plt.subplots(4, figsize=(10,7))
    ax[0].plot(tOut/365.25, f_main_inhs[:,0], label='SOM substrate inhibition', color='k', ls=':')
    ax[0].plot(tOut/365.25, f_pH_inhs[:,0], label='pH inhibition', color='k')
    ax[0].plot(tOut/365.25, f_NH4_tox_inhs[:,0], label=r'$NH_4^+$ toxicity inhibition', color='k',alpha=0.5, ls='--')
    ax[0].plot(tOut/365.25, f_X_inhs[:,0], label=r'biomass presence inhibition', color='k', alpha=0.5, ls=':')
    ax[0].set_title('$\\bf{Hydrolysis}$ $\\bf{lumped}$ $\\bf{with}$ $\\bf{acidogenesis}$ $\\bf{&}$ $\\bf{acetogenesis}$')
    
    ax[1].plot(tOut/365.25, f_main_inhs[:,1], label='acetate substrate inhibition', color='k', ls='--')
    ax[1].plot(tOut/365.25, f_pH_inhs[:,1], label='pH inhibition', color='k')
    ax[1].plot(tOut/365.25, f_NH4_inhs[:,1], label=r'$NH_4^+$ substrate inhibition', color='r', ls='--')
    ax[1].plot(tOut/365.25, f_O2_tox_inhs[:,1], label=r'$O_2$ toxicity inhibition', color='k', alpha=0.5)
    ax[1].set_title('$\\bf{Methanogens}$ $\\bf{growth}$')

    ax[2].plot(tOut/365.25, f_main_inhs[:,2], label='acetate substrate inhibition', color='k', ls='--')
    ax[2].plot(tOut/365.25, f_pH_inhs[:,2], label='pH inhibition', color='k')
    ax[2].plot(tOut/365.25, f_O2_inhs[:,2], label=r'$O_2$ substrate inhibition', color='r')
    ax[2].plot(tOut/365.25, f_NH4_inhs[:,2], label=r'$NH_4^+$ substrate inhibition', color='r', ls='--')
    ax[2].set_title('$\\bf{Oxidizers}$ $\\bf{&}$ $\\bf{Nitrifiers}$ $\\bf{growth}$')

    ax[3].plot(tOut/365.25, f_pH_inhs[:,4], label='pH inhibition', color = 'k')
    ax[3].plot(tOut/365.25, f_main_inhs[:,4], label = 'acetate substrate inhibition', color='k', ls='--')
    ax[3].plot(tOut/365.25, f_main_inhs[:,4]*-1, label='SOM substrate inhibition', color='k', ls=':')
    ax[3].plot(tOut/365.25, f_NH4_inhs[:,4]*-1, label=r'$O_2$ substrate inhibition', color='r')
    ax[3].plot(tOut/365.25, f_NH4_inhs[:,4], label=r'$NH_4^+$ substrate inhibition', color='r', ls='--')
    ax[3].plot(tOut/365.25, f_NO3_inhs[:,4], label = r'$NO_3^-$ substrate inhibition', color='r', ls=':')
    ax[3].plot(tOut/365.25, f_O2_tox_inhs[:,4], label=r'$O_2$ toxicity inhibition', color='k', alpha=0.5)
    ax[3].plot(tOut/365.25, f_main_inhs[:,4]*-1, label = r'$NH_4^+$ toxicity inhibition', color='k',alpha=0.5, ls='--')
    ax[3].plot(tOut/365.25, f_main_inhs[:,4]*-1, label = r'biomass presence inhibition', color='k', alpha=0.5, ls=':')
    
    ax[3].set_title('$\\bf{Denitrifiers}$ $\\bf{growth}$')
    ax[3].legend(bbox_to_anchor=(.9, -.8), ncol=3)

    ax[3].set_xlabel('time (year)')
    ax[0].set_ylabel('f [-]')
    ax[1].set_ylabel('f [-]')
    ax[2].set_ylabel('f [-]')
    ax[3].set_ylabel('f [-]')
    ax[0].set_xlim(0, tOut[-1]/365.25)
    ax[1].set_xlim(0, tOut[-1]/365.25)
    ax[2].set_xlim(0, tOut[-1]/365.25)
    ax[3].set_xlim(0, tOut[-1]/365.25)
    ax[0].set_ylim(0,1.05)
    ax[1].set_ylim(0,1.05)
    ax[2].set_ylim(0,1.05)
    ax[3].set_ylim(0,1.05)
    
    #set ticks:
    ax[0].tick_params(labelbottom=False)
    ax[1].tick_params(labelbottom=False)
    ax[2].tick_params(labelbottom=False)
    #get background 
    for ii in range(len(tOut)-1):
        print(f'plotting... please wait... {ii/(len(tOut)-1) * 100} %')
        for jj in range(4):
                ax[jj].fill_between([tOut[ii]/365.25, tOut[ii+1]/365.25], -0.1,10, color=cmap(norm(O2_act[ii])),zorder=1, lw=0)
    plt.suptitle('Inhibitions for the different reactions', fontsize=20)
    plt.tight_layout()
    plt.savefig('inhibitions_finals.pdf')
    plt.show()


    #### PLOT 2 - porosity - saturation - wastefraction
    fig = plt.figure(constrained_layout=True, figsize=(7,5))
    gs = GridSpec(3, 6, figure=fig)
    ax1 = fig.add_subplot(gs[0, :2])
    ax1.set_title('porosity [-]', fontweight='bold')#$\\bf{porosity} \\bf{[-]}$')
    ax1.set_ylim(0.25,0.35)
    ax2 = fig.add_subplot(gs[0, 2:4])
    ax2.set_title('saturation [-]', fontweight='bold')
    ax2.set_ylim(0.6,1)
    ax3 = fig.add_subplot(gs[0, 4:6])
    ax3.set_title('wastefraction [-]', fontweight='bold')
    ax3.set_ylim(0.2,0.35)
    ax4 = fig.add_subplot(gs[1:3, :3])
    ax4.set_title('total changes', fontweight='bold')
    ax4.set_xlabel('time (year)')
    ax1.set_xlabel('time (year)')
    ax2.set_xlabel('time (year)')
    ax3.set_xlabel('time (year)')
    ax5 = fig.add_subplot(gs[1:3, 3:])
    ax5.set_title('bulk density [kg/$\\bf{m2}$]', fontweight='bold')
    ax5.set_ylim(425,460)
    ax1.set_xlim(0,tOut[-1]/365.25)
    ax2.set_xlim(0,tOut[-1]/365.25)
    ax3.set_xlim(0,tOut[-1]/365.25)
    ax5.set_xlim(0,tOut[-1]/365.25)

    solid_fraction = 1-porosity.T 
    porosity_fraction = porosity.T 
    water_fraction = np.multiply(porosity.T, saturation.T)
    air_fraction = np.multiply(porosity.T, 1-saturation.T)

    waste_degradable = np.multiply(solid_fraction,wastefraction.T)
    waste_inert = solid_fraction - waste_degradable

    bulk_density = np.multiply(solid_fraction , pure_waste_density) + 1000 * water_fraction 
    ax1.plot(tOut/365.25, porosity.T, color='k')
    ax2.plot(tOut/365.25, saturation.T, color='k')
    ax3.plot(tOut/365.25, wastefraction.T, color='k')

    ax4.fill_between(tOut/365.25, waste_degradable.T[0]+waste_inert.T[0], waste_inert.T[0], facecolor='chocolate', alpha=0.8, edgecolor=None, hatch="|", label='degradable waste')
    ax4.fill_between(tOut/365.25, waste_inert.T[0], 0, facecolor='black', alpha=0.8, edgecolor=None, hatch='/', label='inert waste')
    ax4.fill_between(tOut/365.25, waste_inert.T[0] + waste_degradable.T[0] + water_fraction.T[0],  waste_inert.T[0] + waste_degradable.T[0], facecolor='blue', alpha=0.6, edgecolor=None, label='water')
    ax4.fill_between(tOut/365.25, waste_inert.T[0] + waste_degradable.T[0] + water_fraction.T[0] + air_fraction.T[0], waste_inert.T[0] + waste_degradable.T[0] + water_fraction.T[0], facecolor='grey', alpha=0.3, edgecolor=None, label='air')
    ax4.axvline(tOut[-1]/365.25, 0, 1, color='k')
    ax4.axvline(tOut[0]/365.25, 0, 1, color='k')
    ax4.axhline(0, tOut[0]/365.25, tOut[-1]/365.25, color='k')
    ax4.axhline(1, tOut[0]/365.25, tOut[-1]/365.25, color='k')
    ax4.set_xlim(tOut[0]/365.25, tOut[-1]/365.25)
    ax4.set_ylim(0,1)

    ax5.plot(tOut/365.25, bulk_density.T[0], color='k')
    ax5.set_xlabel('time (year)')
    leg = ax4.legend(loc="lower left", framealpha=0.8)

    plt.savefig('fractions_finals.pdf')
    plt.show()

    #### PLOT 3 oxygen INHIBITION ###    
    f_anaerobic_meth = np.array([1-   O2_act /(stoich.params['K_anaerobic'][1])])
    f_anaerobic_meth = f_anaerobic_meth*(f_anaerobic_meth>0) + 0
    f_aerobic_co2 = np.array([O2_act/(stoich.params['K_aerobic'][2]+O2_act)])

    # create figure and axis objects with subplots()
    fig,ax = plt.subplots()
    # make a plot
    ax.plot(tOut/365.25,f_anaerobic_meth[0],color='r', alpha=1, label=('methanogenesis'))
    ax.plot(tOut/365.25,f_aerobic_co2[0], color='b', alpha=1, ls='--', label='acetate to $CO_2$')

    # set x-axis label
    ax.set_xlabel("time (year)", fontsize = 14)
    # set y-axis label
    ax.set_title("$O_2$ inhibition")
    ax.set_ylabel("inhibition factor [-]")
    ax.legend()
    # make a plot with different y-axis using second axis object
    #plt.savefig('inhibitions.pdf')
    plt.show()
    
    
