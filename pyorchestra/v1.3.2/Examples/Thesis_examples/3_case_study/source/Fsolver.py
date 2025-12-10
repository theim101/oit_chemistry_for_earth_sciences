#solver
import numpy as np
import pandas as pd
import scipy.integrate as spi

from source import Fchemical as Fchem
from source import Fwater as Fwat
#import scipy.sparce as sp #use for definition jacobian


def div(t,sBio, sGas, p, sPar, mDim, bPar, stoich):
    """
    Function that calculates and returns the change of the state parameters
    at time step t.
    """
    sBio = np.where(sBio < 0, 1e-20, sBio) #check if a value is below 0 (cant be because ORCHESTRA will fail most of the times) 

    #chemical changes
    R_bio, R_gas = Fchem.FCR(t, sBio, sGas, p, sPar, bPar, stoich)
    
    #water changes
    dtotdt = np.vstack([R_bio, R_gas])
    return dtotdt

def solver(tRange, sVecIni, p, sPar, mDim, bPar, stoich):
    """
    Function that solves the problem at hand based on input values (iniSt) 
    and a given time period (tRange)
    """
    def dYdt(t, sVec):
        if len(sVec.shape) == 1:
            sVec = sVec.reshape(len(sVecIni[0])*mDim.nN,1)
        nN= mDim.nN
        #unpack states
        sBio = sVec[:-2]
        sGas = sVec[-2:]

        rates = div(t, sBio, sGas, p, sPar, mDim, bPar, stoich)
        return rates

    t_span = [tRange[0], tRange[-1]]
    iniSt = np.array([sVecIni.squeeze()])
    int_result = spi.solve_ivp(dYdt, t_span, iniSt[0],
                               method='BDF', vectorized=True, jac=None,
                               t_eval=tRange, rtol=1e-8)
    #check for first 
    return int_result

