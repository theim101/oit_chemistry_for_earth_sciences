

"""import modules"""
#standard packages
import numpy as np
import matplotlib.pyplot as plt
import sys
import csv
import matplotlib
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import ScalarFormatter

#ORCHESTRA PACKAGE
import PyORCHESTRA

#personal packages
from source import Fsolver as Fsol
from source import Forchestra as Forch
from source import Fparameters as Fparam

Kd1 = -4
Kd2 = -1
Kd3 = 0 
Kd4 = 2 
Kds = np.array([Kd1, Kd2, Kd3, Kd4])

results = []
for Kd in Kds:
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
    newline2 = '@logKreaction(NH4_ads, ' + str(Kd) + ', "0.8, 1.0" , NH4+)\n'
    #===================================================================
    #change waste composition in chemistry file:
    with open(input_file) as f:
        data = f.readlines()
        line_number = 0
        for line in data:
            line_number +=1
            if '@composition(waste' in line:
                data[line_number-1] = newline 
            elif '@logKreaction(NH4_ads' in line:
                data[line_number-1] = newline2  

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
    p, IN = Forch.ORCHESTRA_ini(input_file, reaction_file, mDim)

    # =============================================================================
    # 3. initial conditions
    # =============================================================================
    tOut = np.linspace(0, 365.25*60, 3000) #time range (start, end, how many saved points)

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
    IN[np.where(IN == 'waste.tot')]  =  total_organic_waste * 1000/molar_mass_waste #0.778
    IN[np.where(IN == 'acetate.tot')]  = 1.0e-9 # 1.0e-7 
    IN[np.where(IN == 'methanogens.tot')]  = 0.01 # 0.01 
    IN[np.where(IN == 'oxidizers.tot')]  = 0.01 # 0.01 
    IN[np.where(IN == 'nitrifiers.tot')]  = 0.01 # 0.01 
    IN[np.where(IN == 'denitrifiers.tot')]  = 0.01 # 0.01 
    IN[np.where(IN == 'O2.tot')] = 0.0051
    IN[np.where(IN == 'porosity')]  =0.25
    IN[np.where(IN == 'saturation')]  =0.9
    IN[np.where(IN == 'wastefraction')]  = organic_waste_fraction 
    print(total_organic_waste * 1000/molar_mass_waste)
    print(IN)
    sVecIni_bio = np.array([IN]).astype('float32') #get initial value)
    #check if initial configuration is okay (if not, ORCHESTRA will raise an error)
    OUT_first_test = p.set_and_calculate(sVecIni_bio)
    print(OUT_first_test)
    sVecIni = np.concatenate((sVecIni_bio, sVecIni_gas), axis=1) #combine initial vectors (gas and orchestra tots)

    if plot == 'yes':
        # =============================================================================
        # 4. start solving!
        # =============================================================================
        int_result =Fsol.solver(tOut, sVecIni, p, sPar, mDim, bPar, stoich) #run ODE solver

        results.append(int_result)

### PLOT 1 - COMPONENTS ###
fig, ax = plt.subplots(4,2, figsize=(10,7))
fig.suptitle('Effects of Kd for a system with $NH_4^+$ adsorption', fontsize=20)
linestl = ['-', '-','-','-','-','-']
alpha = [1, 1, 1, 1,1,1]
colors= ['k','blue','red','green','c','k']
labels = ['$K_d$ = -4','$K_d$ = -1', '$K_d$ = 0', '$K_d$ = 2']
csvfile = ['Kdminus4', 'Kdminus','Kd1', 'Kd4']
for ii, int_result in enumerate(results):
    newline2 = '@logKreaction(NH4_ads, ' + str(Kds[ii]) + ', "0.8, 1.0" , NH4+)\n'
    with open(input_file) as f:
        data = f.readlines()
        line_number = 0
        for line in data:
            line_number +=1
            if '@logKreaction(NH4_ads' in line:
                data[line_number-1] = newline2  

    #and save the file again with the new composition
    with open(input_file, 'w') as file:
        file.writelines( data )

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
    #p, IN = Forch.ORCHESTRA_ini(input_file, reaction_file, mDim)
    
    pH = []
    O_act = []
    O2_act = []
    ammonium_aq = []
    ammonium_ad = []
    NO3_aq=[]
    p, IN = Forch.ORCHESTRA_ini(input_file, reaction_file, mDim)

    for sBio in int_result.y[mDim.nN*0:mDim.nN*16].T:

        IN = np.array([sBio])
        IN = np.where(IN < 0, 1e-15, sBio)

        OUT = p.set_and_calculate(IN)
        pH.append(OUT[0][16])
        O_act.append(10**OUT[0][15])
        O2_act.append(10**OUT[0][8])
        ammonium_aq.append(10**OUT[0][6])
        NO3_aq.append(10**OUT[0][7])
        ammonium_ad.append(OUT[0][17] * IN[0,-3]*IN[0,-2]/((1-IN[0,-3])))

    cmap = plt.cm.cool 
    norm = matplotlib.colors.Normalize(vmin=min(O2_act), vmax=max(O2_act))
    
    ax[0,0].plot(tOut/365.25, Waste1.T, color=colors[ii],zorder=2, alpha=alpha[ii], ls=linestl[ii], linewidth=1, label = labels[ii])
    ax[0,0].set_title('$\\bf{SOM}$')
    ax[0,0].set_ylabel('[mol]')
    ax[1,0].plot(tOut/365.25, O2_act, color=colors[ii] , alpha=alpha[ii], ls=linestl[ii], linewidth=1)
    ax[1,0].set_title('$\\bf{O_2^{aq}}$')
    ax[1,0].set_ylabel('[mol/L]')
    ax[2,0].plot(tOut/365.25, pH, color=colors[ii], alpha=alpha[ii], ls=linestl[ii], linewidth=1)
    ax[2,0].set_title('$\\bf{pH}$')
    ax[2,0].set_ylabel('[-]')
    ax[0,1].plot(tOut/365.25, ammonium_aq, linewidth=1, ls=linestl[ii], color=colors[ii], alpha=alpha[ii])
    ax[0,1].set_title('$\\bf{NH_{4,aq}^+}$')
    ax[0,1].set_ylabel('[mol/L]')
    ax[1,1].plot(tOut/365.25, NO3_aq, linewidth=1, ls=linestl[ii], color=colors[ii])    
    ax[1,1].set_title('$\\bf{NO_3^-}$')
    ax[1,1].set_ylabel('[mol/L]')
    ax[2,1].plot(tOut/365.25, ammonium_ad, color=colors[ii], alpha=alpha[ii], ls=linestl[ii], linewidth=1)
    ax[2,1].set_title('$\\bf{NH_{4,ad}^+}$')
    ax[2,1].set_ylabel('[mol/L]')
    ax[3,1].plot(tOut/365.25, CH4.T, color=colors[ii], alpha=alpha[ii], ls=linestl[ii], linewidth=1)
    ax[3,1].set_title('$\\bf{CH_4}$')
    ax[3,1].set_ylabel('[mol]')
    ax[3,0].plot(tOut/365.25, CO2.T, color=colors[ii], alpha=alpha[ii], ls=linestl[ii], linewidth=1)
    ax[3,0].set_title('$\\bf{CO_2}$')    
    ax[3,0].set_ylabel('[mol]')
    ax[0,0].legend(loc='upper right', fontsize='x-small')
    
    #y limits:
    #y limits:
#    ax[0,0].set_ylim(min(Waste1.T)-0.05*np.mean(Waste1), max(Waste1.T)+0.05*np.mean(Waste1.T))
#    ax[1,0].set_ylim(min(acetate.T)-0.05*np.mean(acetate), max(acetate.T)+0.05*np.mean(acetate.T))
#    ax[2,0].set_ylim(min(biomass1.T)-0.05*np.mean(biomass1), max(biomass2.T)+0.05*np.mean(biomass2.T))
#    ax[3,0].set_ylim(min(pH)-0.05*np.mean(pH), max(pH)+0.05*np.mean(pH))
#    ax[0,1].set_ylim(min(ammonium_aq)-0.05*np.mean(ammonium_aq), max(ammonium_aq)+0.05*np.mean(ammonium_aq))
#    ax[1,1].set_ylim(min(O2_act)-0.05*np.mean(O2_act), max(O2_act)+0.05*np.mean(O2_act))
#    ax[2,1].set_ylim(min(CO2.T)-0.05*np.mean(CO2), max(CO2.T)+0.05*np.mean(CO2))
#    ax[3,1].set_ylim(min(CH4.T)-0.05*np.mean(CH4), max(CH4.T)+0.05*np.mean(CH4))    
class ScalarFormatterClass(ScalarFormatter):
    def _set_format(self):
        self.format = "%1.2f"
yScalarFormatter = ScalarFormatterClass(useMathText=True)
yScalarFormatter.set_powerlimits((0,0))

for ii in range(4):
    for jj in range(2):
        ax[ii,jj].set_xlim(0,tOut[-1]/365.25)
        ax[ii,jj].yaxis.set_major_formatter(yScalarFormatter)

ax[3,0].set_xlabel('time (year)')
ax[3,1].set_xlabel('time (year)')
plt.tight_layout()
plt.savefig('components_case2b.pdf')
plt.show()

### PLOT 1 - biomass species ###
fig, ax = plt.subplots(4,1, figsize=(7,5))
fig.suptitle('Effects of Kd for a system with $NH_4^+$ adsorption', fontsize=20)
linestl = ['-', '-','-','-','-','-']
alpha = [1, 1, 1, 1,1,1]
colors= ['k','blue','red','green','c','k']
labels = ['$K_d$ = -4', '$K_d$=-1','$K_d$ = 1', '$K_d$ = 2', '1:50']

for ii, int_result in enumerate(results):
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
    #p, IN = Forch.ORCHESTRA_ini(input_file, reaction_file, mDim)
    
    #set background for first three plots
   
    ax[0].plot(tOut/365.25, methanogens.T, color=colors[ii],zorder=2, alpha=alpha[ii], ls=linestl[ii], linewidth=1, label = labels[ii])
    ax[0].set_title('$\\bf{Methanogens}$')
    ax[0].set_ylabel('[mol/L]')
    ax[1].plot(tOut/365.25, oxidizers.T, color=colors[ii] , alpha=alpha[ii], ls=linestl[ii], linewidth=1,label = labels[ii])
    ax[1].set_title('$\\bf{Oxidizers}$')
    ax[1].set_ylabel('[mol/L]')
    ax[2].plot(tOut/365.25, nitrifiers.T, color=colors[ii], alpha=alpha[ii], ls=linestl[ii], linewidth=1, label = labels[ii])
    ax[2].set_title('$\\bf{Nitrifiers}$')
    ax[2].set_ylabel('[mol/L]')
    ax[3].plot(tOut/365.25, denitrifiers.T, color=colors[ii], alpha=alpha[ii], ls=linestl[ii], linewidth=1, label = labels[ii])
    ax[3].set_title('$\\bf{Denitrifiers}$')
    ax[3].set_ylabel('[mol/L]')
    ax[0].legend(loc='upper right', fontsize='small')
    
    ax[0].set_ylim(0,0.125)
    ax[1].set_ylim(0,0.07)
    ax[2].set_ylim(0,0.05)
    ax[3].set_ylim(0,0.075)
ax[0].tick_params(labelbottom=False)
ax[1].tick_params(labelbottom=False)
ax[2].tick_params(labelbottom=False)

for ii in range(4):
    ax[ii].set_xlim(0,tOut[-1]/365.25)
    ax[ii].yaxis.set_major_formatter(yScalarFormatter)
ax[3].set_xlabel('time (year)')
plt.tight_layout()
plt.savefig('Case_4b_biomass.pdf')
plt.show()


