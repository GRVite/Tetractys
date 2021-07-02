#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 17:11:23 2021

@author: vite
"""
from functions import *
from wrappers import *
from my_functions import *
import matplotlib.pyplot as plt
import neuroseries as nts
import pandas as pd
import pickle5 as pickle
import os


data_directory_load = '/Users/vite/OneDrive - McGill University/PeyracheLab/Data/A7701/A7701-210211/my_data'
dir2save = data_directory_load
dir2save_plots = os.path.join(data_directory_load, 'my_data', 'plots') 
session = 'A7701-210211'
# load data
spikes = pickle.load(open(data_directory_load + '/spikes.pickle', 'rb'))
shank = pickle.load(open(data_directory_load  + '/shank.pickle', 'rb'))
episodes = pickle.load(open(data_directory_load + '/episodes.pickle', 'rb'))
position = pickle.load(open(data_directory_load  + '/position.pickle', 'rb'))
wake_ep = pickle.load(open(data_directory_load  + '/wake_ep.pickle', 'rb'))
sleep_ep = pickle.load(open(data_directory_load  + '/sleep_ep.pickle', 'rb'))

#Autocorrelations
autocorrs, frates = compute_AutoCorrs(neurons_sel, wake_ep)
autocorrs.rolling(window=10, win_type='gaussian', center = True, min_periods = 1).mean(std = 2.0)
autocorrs.plot(subplots=True)


#Crosscorrelations
cc_wake = compute_CrossCorrs(neurons_sel, wake_ep, norm=True)
cc_sleep = compute_CrossCorrs(neurons_sel, sleep_ep, 0.25, 200, norm=True)
cc_wake = cc_wake.rolling(window=20, win_type='gaussian', center = True, min_periods = 1).mean(std = 4.0)
cc_sleep = cc_sleep.rolling(window=20, win_type='gaussian', center = True, min_periods = 1).mean(std = 4.0)
cc_wake.plot(subplots=True)
cc_sleep.plot(subplots=True)