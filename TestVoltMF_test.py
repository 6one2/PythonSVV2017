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
#datafile = ['MF020_Steps.lvm']
Coef = np.zeros([len(datafile),2])

for count, fname in enumerate(datafile):
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
    idxSP=idxPeak[ii+1];
    idxEP=idxPeak[ii[1:]];idxEP = np.append(idxEP,idxPeak[-1])
    resP1 = np.zeros([len(idxSP),2]);ct=0
    
    for st, en in zip(idxSP, idxEP):
        
        section = np.arange(st,en)
        
        # fit linear regression
        if True:
            P = np.polyfit(data.Current[section],data.MF[section],1)
            Y = P[0]*data.Current[section]+P[1]
            
            resP1[ct,0]=P[0];resP1[ct,1]=P[1];ct=ct+1
            
            plt.figure()
            plt.plot(data.Current[section],data.MF[section],'.')
            plt.plot(data.Current[section],Y,'k',linewidth=1)
            plt.title('Y = ' + str(P[0]) + 'X + ' + str(P[1]))
        
        #find a coef for linear regression
        Coef[count,0] = np.mean(resP1[0:len(resP1)-1,0])
        Coef[count,1] = np.mean(resP1[0:len(resP1)-1,1])
        
        
        # sinus simulation for each section
        if False:
            A = data.MF[st]
            w = 20 # 20 Hz signal
            t = data.time[section]-data.time[st]
            Sin = A*np.sin(2*np.pi*w*t+np.pi/2)
            COR = np.corrcoef(Sin,data.MF[section])[0][1]
        
            plt.figure()
            plt.plot(data.time[section],data.MF[section],linewidth=3)
            plt.plot(data.time[section],Sin,'k')
            plt.ylim(-210,210)
            plt.title('R = ' + str(COR))
        
        
    
    

    #graph  
    if False:
#        plt.figure(0)
#        plt.plot(data.time,data.MF)
#        plt.plot(data.time,MFf,'k--',linewidth=1)
        
        
    
#old code
if False:
    #data = np.genfromtxt(readfolder+fname,delimiter='\t',skip_header=24)
    data = pd.read_csv(readfolder+fname,skiprows=23,delimiter='\t')
    data.columns = data.columns=(['time','MF','Current','V','Comment'])