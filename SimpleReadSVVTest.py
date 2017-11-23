#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 14:50:52 2017

@author: sebastienvillard
"""

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import pandas as pd

Fs=10000


readfolder = '/Users/sebastienvillard/Documents/LawsonImaging/Expes/SVV/Test/CoilFieldVoltage/'
files = ['Calib_020Hz_4.4','Calib_060Hz_1.4','Calib_120Hz_0.7','Calib_160Hz_0.5']

fname = files[3]

Fr = int(fname[fname.find('_')+1:fname.find('Hz')])

data = pd.read_csv(readfolder+fname+'.txt',skiprows=23,delimiter='\t')
data.columns = data.columns=(['time','MF','Current','V','Comment'])

data.MF=data.MF*20

## filtering
## butterworth forward-backward
Ny = Fs/2
cutOff = 100
Wn = cutOff/Ny

b, a = signal.butter(4, Wn, 'low')#butterworth 4th oredr
MFf = signal.filtfilt(b, a, data.MF)#forward-backward

## Analysis section
thr=0.5
idxSt = np.where(np.abs(MFf)>thr)[0][0]
idxEn = np.where(np.abs(MFf)>thr)[0][-1]
section = np.arange(idxSt,idxEn)

## Rms value
Brms = np.sqrt(np.mean(data.MF[section]**2))
Irms = np.sqrt(np.mean(data.Current[section]**2))
Vrms = data.V[0]

dBdt = Fr * 2 * np.pi * Brms
print(fname + ' gives ' +str(dBdt))



if True:
    plt.plot(data.time[section],data.MF[section])
