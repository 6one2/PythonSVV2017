#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 16:46:06 2017

@author: sebastienvillard
"""

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import pandas as pd

Fs=10000


readfolder = '/Users/sebastienvillard/Documents/LawsonImaging/Expes/SVV/Test/CoilFieldVoltage/'
files = ['Ref_020','Ref_060','Ref_120','Ref_160','Ref_060_MX']
ext='.lvm'

fname = files[3]

Fr = int(fname[fname.find('_')+1:fname.find('_')+4])

data = pd.read_csv(readfolder+fname+ext,skiprows=23,delimiter='\t')
data.columns = data.columns=(['time','MF','Current','V','Comment'])

data.MF=data.MF*20 # for ref files probe signal [-10V:+10V] -> transform to mT


## filtering
## butterworth forward-backward
Ny = Fs/2
cutOff = 100
Wn = cutOff/Ny

b, a = signal.butter(4, Wn, 'low')#butterworth 4th oredr
MFf = signal.filtfilt(b, a, data.MF)#forward-backward

## Analysis section
thr=10
idxSt = np.where(np.abs(data.Current)>thr)[0][0]
idxEn = np.where(np.abs(data.Current)>thr)[0][-1]
section = np.arange(idxSt,idxEn)

## Rms value
Brms = np.sqrt(np.mean(data.MF[section]**2))
Irms = np.sqrt(np.mean(data.Current[section]**2))
Vrms = data.V[0]

dBdt = Fr * 2 * np.pi * Brms
print(fname + ' gives ' +str(dBdt))



if True:
    plt.plot(data.time[section],data.MF[section])
