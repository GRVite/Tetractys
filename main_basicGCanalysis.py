#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 10:56:49 2019-

@author: vite


"""


"""
This script will show you how to load the various data you need

The function are already written in the file wrappers.py that should be in the same directory as this script

To speed up loading of the data, a folder called /Analysis will be created and some data will be saved here
So that next time, you load the script, the wrappers will search in /Analysis to load faster
"""
import os
import numpy as np
import pandas as pd
import neuroseries as nts
#from pylab import *
import matplotlib.pyplot as plt
from functions import *
from scipy.ndimage import gaussian_filter
from scipy.signal import correlate2d
import pickle5 as pickle



"""
A. LOAD DATA
"""

# def analysis(data_directory_load, dir2save_plots, ID, session):
# data_directory_load = '/Users/vite/navigation_system/Data/A6100/A6100-201026'
data_directory_load = '/Users/vite/OneDrive - McGill University/PeyracheLab/A7701/A7701-210217/my_data'
# data_directory_load = OneD
# load data
spikes = pickle.load(open(data_directory_load + '/spikes.pickle', 'rb'))
shank = pickle.load(open(data_directory_load  + '/shank.pickle', 'rb'))
episodes = pickle.load(open(data_directory_load + '/episodes.pickle', 'rb'))
position = pickle.load(open(data_directory_load  + '/position.pickle', 'rb'))
wake_ep = pickle.load(open(data_directory_load  + '/wake_ep.pickle', 'rb'))


dir2save_plots = data_directory_load + '/plots'
if not os.path.exists(dir2save_plots):
    os.mkdir(dir2save_plots)




"""
GENERAL
"""

###
#Place fields
###

numNeurons = len (spikes.keys())
NeurNShank = []
for s in np.unique(shank):
    for n in range(sum(shank==s)):
        NeurNShank.append(n)
sigma = 1.2
GF, ext = computePlaceFields(spikes, position[['x', 'z']], wake_ep, 30)
if numNeurons < 30:
    raws = round(len(spikes)/5)
    plt.figure(figsize=(50,60))
    for i,k in enumerate(GF.keys()):
        plt.subplot(5,raws+1,i+1)    
        tmp = gaussian_filter(GF[k].values, sigma = sigma)
        im=imshow(tmp, extent = ext, cmap = 'jet', interpolation = 'bilinear')
        #plt.colorbar(im,fraction=0.046, pad=0.04)
        plt.title(str([i]))
        plt.xticks([]),plt.yticks([])
        plt.colorbar()
    plt.show()
    plt.suptitle('Place fields ' + session)
    plt.savefig(dir2save_plots + '/GF'+str(sigma)+'.png')
else:
    groups = int(ceil(numNeurons/30))
    start = 0
    stop = 30
    it = [*range(groups)]
    for g in it:
        selection = range(start,stop)
        print("selection",selection)
        plt.figure(figsize=(40,200))
        for i, n in enumerate(selection):
            plt.subplot(4,8,i+1)    
            tmp = gaussian_filter(GF[n].values, sigma = sigma)
            im=imshow(tmp, extent = ext, cmap = 'jet', interpolation = 'bilinear')
            #plt.colorbar(im,fraction=0.046, pad=0.04)
            plt.title('Neuron' + ' ' + str(NeurNShank[n]) + ' shank_' +str(shank[n]), loc ='center', pad=25)
            plt.xticks([]),plt.yticks([])
            plt.colorbar()
            plt.subplots_adjust(wspace=0.4, hspace=2, top = 0.85)
            plt.show()
            plt.savefig(dir2save_plots + '/GC' + str(g) +'.pdf')
        plt.figure(figsize=(40,50))
        for i,k in enumerate(selection):
            plt.subplot(4,8,i+1)
            tmp = gaussian_filter(GF[k].values, sigma = 0.5)
            tmp2 = correlate2d(tmp, tmp)
            imshow(tmp2, extent = ext, cmap = 'jet', interpolation = 'bilinear')
            plt.title('Neuron' + ' ' + str(NeurNShank[k]) + ' shank_' +str(shank[k]), loc ='center', pad=25)
        plt.savefig(dir2save_plots + '/Au.pdf'+ str(g) +'.pdf')
        start+= 30
        stop+=30
        if g == it[-2]:
            stop  = numNeurons
