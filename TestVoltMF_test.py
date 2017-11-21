#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 09:29:21 2017

@author: sebastienvillard
"""

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import pandas as pd

Fs=10000


readfolder = '/Users/sebastienvillard/Documents/LawsonImaging/Expes/SVV/Test/CoilFieldVoltage/'
datafile = ['MF020_High.lvm','MF060_High.lvm','MF020_Steps.lvm','MF060_Steps.lvm',]
datafile = ['MF020_Steps.lvm']

for fname in datafile:
    print(readfolder+fname)
    data = pd.read_csv(readfolder+fname,skiprows=23,delimiter='\t')
    data.columns = data.columns=(['time','MF','Current','V','Comment'])
    
    ## filtering
    ## butterworth forward-backward
    Ny = Fs/2
    cutOff = 100
    Wn = cutOff/Ny
    
    b, a = signal.butter(4, Wn, 'low')#butterworth 4th oredr
    MFf = signal.filtfilt(b, a, data.MF)#forward-backward
    
    
    ## peak detection
    k=100
    idxPeak_k = signal.find_peaks_cwt(MFf,np.arange(1,k))
    idxPeak = idxPeak_k[MFf[idxPeak_k]>100]
    
    
    ## find transition of B.
    thr=2.5
    ii = np.flatnonzero(np.diff(data.MF[idxPeak])>thr)#look for transition in max MF
    idxGP=idxPeak(ii)+1
    
    # check np.polyfit for linear regression

    #graph  
    if True:
#        plt.figure(0)
#        plt.plot(data.time,data.MF)
#        plt.plot(data.time,MFf,'k--',linewidth=1)
        
        plt.figure(1)
        plt.plot(data.time,data.MF)
        plt.plot(data.time[idxPeak], data.MF[idxPeak],'ko')
        plt.plot(data.time[idxGP], data.MF[idxGP],'ro')
        
        plt.figure(3)
        PP = plt.plot(np.diff(data.MF[idxPeak]),'.-',markercolor='k')
        plt.plot(np.diff(data.MF[idxPeak]),'.-')
        
    
#old code
if False:
    #data = np.genfromtxt(readfolder+fname,delimiter='\t',skip_header=24)
    data = pd.read_csv(readfolder+fname,skiprows=23,delimiter='\t')
    data.columns = data.columns=(['time','MF','Current','V','Comment'])