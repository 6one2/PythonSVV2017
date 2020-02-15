# check the magnetic field generated at each experimental condition
# recordings from medium local coil (Labview)
import numpy as np
from scipy import signal, fftpack
import matplotlib.pyplot as plt
from pylab import rcParams
import pandas as pd

rcParams['figure.figsize'] = 10, 7

Fs = 10000 # Sampling Rate


readfolder = './Ref_files/'
Files = ('Ref_020', 'Ref_060', 'Ref_120', 'Ref_160', 'Ref_060_MX')
ext = '.lvm'

# fname = Files[3]
for i, fname in enumerate(Files):
         
    Fr = int(fname.split('_')[1])  # Stimulation Frequency

    data = pd.read_csv(readfolder+fname+ext,skiprows=23,delimiter='\t')
    data.columns = data.columns=(['time','MF','Current','V','Comment'])

    data.MF=data.MF*20  # for ref files probe signal [-10V:+10V] -> transform to mT


    ## filtering
    ## butterworth forward-backward
    Ny = Fs/2
    cutOff = 100
    Wn = cutOff/Ny

    b, a = signal.butter(4, Wn, 'low')  # butterworth 4th order
    MFf = signal.filtfilt(b, a, data.MF)  # forward-backward

    ## Analysis section
    thr=10
    idxSt = np.where(np.abs(data.Current)>thr)[0][0]
    idxEn = np.where(np.abs(data.Current)>thr)[0][-1]
    all_sample = np.arange(idxSt, idxEn)
    section = np.arange(idxSt, idxSt+1*Fs)
    
    ## Fast Fourier Transform
    Y = fftpack.fft(data.MF)
    fft_freq = fftpack.fftfreq(len(data.MF), 1/Fs)
    idx_pos = fft_freq > 0

    ## Rms value
    B_rms = np.sqrt(np.mean(data.MF[all_sample]**2))  # Magnetic Field Density, T (rms), measured against coil (0,0,0)
    I_rms = np.sqrt(np.mean(data.Current[all_sample]**2))  # Intensity, A (rms), output from amplifier to coil
#     V_command = data.V[0]  # Volt, V: command to amplifiers

    dBdt = Fr * 2 * np.pi * B_rms / 1000  # T/s
    lab = f'{Fr} Hz'
    title = f'{dBdt:.2f} $T.s^{-1}$'


    if True:
        plt.figure(1)
        plt.subplot(1,len(Files),i+1)
        plt.plot(data.time[section],data.MF[section], label = lab)
        plt.ylim(-200, 200)
        plt.ylabel('B (mT)')
        plt.xlabel('Time (s)')
        plt.title(title)
        plt.legend(loc=1)
        
        plt.figure(2)
        plt.subplot(1,len(Files),i+1)
        plt.plot(fft_freq[idx_pos], np.abs(Y[idx_pos])**2,'.-')
        plt.xlim(0,200)

plt.show()