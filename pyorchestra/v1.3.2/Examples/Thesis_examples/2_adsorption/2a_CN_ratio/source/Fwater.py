#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
#Fwater
"""include code Timo for time travel distribution"""
"""right now, nothing is done with this"""

def Fwater_in(t): #rainfall in mm 
    qin = 0.0001 #0.001 #+ 0.0001*math.cos(t/1000)
            #bndT = bPar.avgT - bPar.rangeT * np.cos(2 * np.pi * (t - bPar.tMin)
            #                                        / 365.25)
    return qin

def Fwater_out(t): #water extraction in mm
    qout = 0.0001 #0.001# + 0.000025*math.cos(t/1000)
    return qout

def Fq_tot(t):
    q_in = Fwater_in(t)
    q_out = Fwater_out(t)
    q_tot = q_in-q_out
    return q_tot


