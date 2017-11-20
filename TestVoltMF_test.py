#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 09:29:21 2017

@author: sebastienvillard
"""

import numpy as np
#import os
import matplotlib.pyplot as plt
import pandas as pd

Fs=10000


readfolder = '/Users/sebastienvillard/Documents/LawsonImaging/Expes/SVV/Test/CoilFieldVoltage/'
datafile = ['MF020_High.lvm','MF060_High.lvm','MF020_Steps.lvm','MF060_Steps.lvm',]
datafile = ['MF020_High.lvm']

for fname in datafile:
    print(readfolder+fname)
    data = pd.read_csv(readfolder+fname,skiprows=23,delimiter='\t')
    data.columns = data.columns=(['time','MF','Current','V','Comment'])
    
    ## filtering
    
    ## peak detection
    
    ## 
    
    # check np.polyfit for linear regression

    #graph  
    if False:
        plt.figure()
        plt.subplot(311)
        plt.plot(data.time,data.MF,'r-');plt.title(fname)
        plt.subplot(312)
        plt.plot(data.time,data.Current,'r-')
        plt.subplot(313)
        plt.plot(data.Current,data.MF,'ko')
        
        plt.show()
    
#old code
if False:
    #data = np.genfromtxt(readfolder+fname,delimiter='\t',skip_header=24)
    data = pd.read_csv(readfolder+fname,skiprows=23,delimiter='\t')
    data.columns = data.columns=(['time','MF','Current','V','Comment'])