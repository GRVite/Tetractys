#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 25 23:24:59 2021

@author: vite
"""


aucorr_w, fr_w = compute_AutoCorrs(spikes, wake_ep, 5, 100) #binsize?
aucorr_s = (spikes, wake_ep, 5, 100)

if numNeurons < 30:
    raws = round(len(spikes)/5)
    plt.figure(figsize=(50,60))
    for i,k in enumerate(GF.keys()):
        plt.subplot(5,raws+1,i+1)    
        tmp = aucorr_w[k]
        plt.plot(tmp)
        #plt.colorbar(im,fraction=0.046, pad=0.04)
        plt.title(str([i]))
        plt.xticks([]),plt.yticks([])
    plt.show()
    
    