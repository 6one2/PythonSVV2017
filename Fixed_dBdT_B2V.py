#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 10:52:30 2017

@author: sebastienvillard
"""

import numpy as np


readfolder = '/Users/sebastienvillard/Documents/LawsonImaging/Expes/SVV/Test/CoilFieldVoltage/'
resfile = 'ResCoef.txt'
Frequencies = np.array([20,60,120,160])


COEF = np.loadtxt(readfolder+resfile)
a = np.mean(COEF[:,0])
b = np.mean(COEF[:,1])

# B = aI + b

Vmax = 4.4
Imax = Vmax * 43

Bmax = a * Imax + b

FixdBdT = 2 * np.pi * Bmax * Frequencies[0] #max dB/dT for 4.4 V @ 20 Hz

Res = np.zeros([len(Frequencies),4])
Res[0,:] = [Bmax, Imax, Vmax, FixdBdT]

# compute voltage -> FixdBdT @ other frequencies
for k,fr in enumerate(Frequencies[1:,]):
    B = FixdBdT/(2 * np.pi * fr)
    dBdT = 2 * np.pi * B * fr
    #print('B field is ' + str(B) + ' dB/dt is ' + str(dBdT))
    I = B/a - b; V = I/43
    
    Res[k+1,:] = [B, I, V, dBdT]