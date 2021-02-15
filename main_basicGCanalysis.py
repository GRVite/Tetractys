#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 10:56:49 2019-

@author: vite

Based on main4_raw, Starter Pack, Guillaume Viejo
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
data_directory_load = '/Users/vite/OneDrive - McGill University/PeyracheLab/A7701/A7701-210211/my_data'
# data_directory_load = OneD
# load data
spikes = pickle.load(open(data_directory_load + '/spikes.pickle', 'rb'))
shank = pickle.load(open(data_directory_load  + '/shank.pickle', 'rb'))
episodes = pickle.load(open(data_directory_load + '/episodes.pickle', 'rb'))
position = pickle.load(open(data_directory_load  + '/position.pickle', 'rb'))
wake_ep = pickle.load(open(data_directory_load  + '/wake_ep.pickle', 'rb'))
# opto_ep = pickle.load(open(data_directory_load  + '/opto_ep.pickle', 'rb'))
# stim_ep = pickle.load(open(data_directory_load  + '/stim_ep.pickle', 'rb'))

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
        # plt.figure(figsize=(40,200))
        # for i, n in enumerate(selection):
        #     plt.subplot(4,8,i+1)    
        #     tmp = gaussian_filter(GF[n].values, sigma = sigma)
        #     im=imshow(tmp, extent = ext, cmap = 'jet', interpolation = 'bilinear')
        #     #plt.colorbar(im,fraction=0.046, pad=0.04)
        #     plt.title('Neuron' + ' ' + str(NeurNShank[n]) + ' shank_' +str(shank[n]), loc ='center', pad=25)
        #     plt.xticks([]),plt.yticks([])
        #     plt.colorbar()
        #     plt.subplots_adjust(wspace=0.4, hspace=2, top = 0.85)
        #     plt.show()
        #     plt.savefig(dir2save_plots + '/GC' + str(g) +'.pdf')
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

selection = range(47,115,1)
plt. figure(figsize=(50,60))
for i,k in enumerate(selection):
    plt.subplot(10,7,i+1)    
    tmp = gaussian_filter(GF[k].values, sigma = 1)
    im=imshow(tmp, extent = ext, cmap = 'jet', interpolation = 'bilinear')
    #plt.colorbar(im,fraction=0.046, pad=0.04)
    plt.xticks([])
    plt.yticks([])
    # plt.title(str(k))
plt.show()
plt.savefig(dir2save_plots + '/GF_selected.pdf')

###
#Autocorrelograms
###
plt.figure(figsize=(40,50))
for i,k in enumerate(selection):
    plt.subplot(10,raws+1,i+1)
    tmp = gaussian_filter(GF[k].values, sigma = 1)
    tmp2 = correlate2d(tmp, tmp)
    imshow(tmp2, extent = ext, cmap = 'jet', interpolation = 'bilinear')
    # plt.title(str([i]))
plt.savefig(dir2save_plots + '/Au.pdf')

#Test rotate
from scipy import ndimage, misc
ndimage.rotate(tmp2, 45, reshape=True)

plt.figure(figsize=(4,5))
tmp = gaussian_filter(GF[2].values, sigma = 0.35)
tmp2 = correlate2d(tmp, tmp)
imshow(tmp2, cmap = 'jet', interpolation = 'bilinear')
plt.colorbar(im,fraction=0.046, pad=0.04)
plt.title(str([i]))
plt.scatter(peaks[1:,0],peaks[1:,1], marker="*",c='black')
plt.plot([29,39])

#test identify peaks
from skimage.feature import peak_local_max
peaks = peak_local_max(tmp2, num_peaks = 7)


#Spike maps
plt.figure(figsize = (15,16))
#fig.subtitle('Spikes + Path Plot',size=30)
for i,k in enumerate(selection):
    ax=subplot(7,10,i+1) #if you have more than 20cells change the numbers in bracket to reflect that
    plt.scatter(position['x'].realign(spikes[k].restrict(wake_ep)),position['z']
                .realign(spikes[k].restrict(wake_ep)),s=5,c='steelblue',label=str(k))
    legend()
    plt.plot(position['x'].restrict(wake_ep),position['z'].restrict(wake_ep),color='lightgrey', alpha=0.5)  


"""
Place fields of the first x minutes of activity for a given neuron
"""
#Select a neuron
n=87
minutes=15xt(0.5, 0.01, str(minutes) + ' min')
plt.colorbar(im,fraction=0.046, pad=0.04)
ax2.invert_yaxis()  
            
ax3=subplot(2,2,3)
plt.plot(nposition['x'], nposition['z'])
plt.title("Tracking data")

ax4=subplot(2,2,4)
tmp = gaussian_filter(GFu[0].values, sigma = 1.1)
im=imshow(tmp, extent = ext1, cmap = 'jet', interpolation = 'bilinear')
plt.title("N
start = wake_ep.start[0]
end = start+ minutes* 60000000
interval = nts.IntervalSet(start = start, end = end)
dic = {0:spikes[n].restrict(interval)}
nposition = position[['x', 'z']].restrict(interval)
GFu, ext1 = computePlaceFields(dic, nposition , wake_ep, 30)

plt. figure(figsize=(10,30))
ax1=subplot(2,2,1)
plt.plot(position['x'], position['z'])
plt.title("Tracking data")
ax2=subplot(2,2,2)
tmp = gaussian_filter(GF[n].values, sigma = 1.1)
im=imshow(tmp, extent = ext, cmap = 'jet', interpolation = 'bilinear')
plt.title("Neuron " + str(n))
plt.gcf().teeuron " + str(n))
plt.gcf().text(0.5, 0.01, str(minutes) + ' min')
plt.colorbar(im,fraction=0.046, pad=0.04)
ax4.invert_yaxis()

"""
Place fields 
"""

#First half
duration = spikes[n].end_time() - spikes[n].start_time()
start = spikes[n].start_time()
end = spikes[n].start_time()+ duration/2
interval = nts.IntervalSet(start = start, end = end)
dic = {0:spikes[n].restrict(interval)}
nposition1 = position[['x', 'z']].restrict(interval)
GFu1, ext1 = computePlaceFields(dic, nposition1 , wake_ep, 30)

#Second half
start = spikes[n].start_time()+ duration/2
end = spikes[n].end_time()
interval = nts.IntervalSet(start = start, end = end)
dic = {0:spikes[n].restrict(interval)}
nposition2 = position[['x', 'z']].restrict(interval)
GFu2, ext2 = computePlaceFields(dic, nposition2 , wake_ep, 30)

#Plots
plt. figure(figsize=(8,40))
ax1=subplot(3,2,1)
plt.plot(position['x'], position['z'])
plt.title(str(int(duration/1000/1000/60)) + " min")
ax2=subplot(3,2,2)
tmp = gaussian_filter(GF[n].values, sigma = 1.1)
im=imshow(tmp, extent = ext, cmap = 'jet', interpolation = 'bilinear')
plt.title("Complete")
plt.colorbar(im,fraction=0.046, pad=0.04)
ax2.invert_yaxis()  

ax3=subplot(3,2,3)
plt.plot(nposition1['x'], nposition1['z'])
plt.title("0 - " + str(int(duration/1000/1000/60/2)) + " min")
ax4=subplot(3,2,4)
tmp = gaussian_filter(GFu1[0].values, sigma = 1.1)
im=imshow(tmp, extent = ext1, cmap = 'jet', interpolation = 'bilinear')
plt.title("First half")
plt.colorbar(im,fraction=0.046, pad=0.04)
ax4.invert_yaxis()  

ax5=subplot(3,2,5)
plt.plot(nposition2['x'], nposition2['z'])
plt.title(str(int(duration/1000/1000/60/2)) + " - " +str(int(duration/1000/1000/60)) + " min")
ax6=subplot(3,2,6)
tmp = gaussian_filter(GFu2[0].values, sigma = 1.1)
im=imshow(tmp, extent = ext2, cmap = 'jet', interpolation = 'bilinear')
plt.title("Second half")
plt.colorbar(im,fraction=0.046, pad=0.04)
ax6.invert_yaxis()  

plt.tight_layout()
plt.suptitle("Comparisson ", x = 0.5, y = 1)
plt.savefig(data_directory + '/plots' + '/Comparisson.pdf')



"""
Summary figure for one neuron 
"""
#Select a neuron
n=84
plt. figure(figsize=(10,30))

ax1=subplot(2,2,1)
ax1.set_axis_off()
plt.plot(position['x'], position['z'], c='steelblue',)
plt.title("A", loc ='left',fontsize=25)
plt.box(False)

ax2=subplot(2,2,2)
ax2.invert_yaxis()  
ax2.set_axis_off()
tmp = gaussian_filter(GF[n].values, sigma = 2)
im=imshow(tmp, extent = ext, cmap = 'jet', interpolation = 'bilinear')
plt.title("B", loc ='left',fontsize=25)
plt.colorbar(im,fraction=0.046, pad=0.04)
plt.box(False)
            
ax3=subplot(2,2,3)
ax3.set_axis_off()
plt.scatter(position['x'].realign(spikes[n].restrict(wake_ep)),position['z'].
            realign(spikes[n].restrict(wake_ep)), s=5, c='steelblue', label=str(n))
plt.plot(position['x'].restrict(wake_ep),position['z'].restrict(wake_ep),color='lightgrey', alpha=0.5)  
plt.title("C", loc ='left',fontsize=25)
plt.box(False)

ax4=subplot(2,2,4)
tmp = gaussian_filter(GF[n].values, sigma = 0.5)
tmp2 = correlate2d(tmp, tmp)
imshow(tmp2, extent = ext, cmap = 'jet', interpolation = 'bilinear')
ax4.set_axis_off()
plt.box(False)
plt.title("D", loc ='left',fontsize=25)
plt.suptitle("neuron" + str(n))
plt.savefig(dir2save_plots+ '/figure_proposal_n' + str(n) + '.pdf')
