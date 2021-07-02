#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 13:27:15 2021

@author: vite
"""



from functions import *
from wrappers import *
import matplotlib.pyplot as plt
from my_functions import *
import neuroseries as nts
import pandas as pd
import pickle5 as pickle
import os


# def analysis(data_directory_load, dir2save_plots, ID, session):
data_directory_load = '/Users/vite/OneDrive - McGill University/PeyracheLab/Data/A7701/A7701-210216/my_data'
dir2save = data_directory_load
dir2save_plots = os.path.join(data_directory_load, 'my_data', 'plots') 
session = 'A7701-210216'
# load data
spikes = pickle.load(open(data_directory_load + '/spikes.pickle', 'rb'))
shank = pickle.load(open(data_directory_load  + '/shank.pickle', 'rb'))
episodes = pickle.load(open(data_directory_load + '/episodes.pickle', 'rb'))
position = pickle.load(open(data_directory_load  + '/position.pickle', 'rb'))
wake_ep = pickle.load(open(data_directory_load  + '/wake_ep.pickle', 'rb'))

#make raster plot for one neuron
neuron = 38
length = 5*60e6
raster_list = raster.gendata({str(neuron):spikes[neuron]}, 0, round(wake_ep.start.values[0]+length), wake_ep.start.values)
ephysplots.raster_basic(raster_list, dir2save)
#make it for more than 1 neurons
raster_list = raster.gendata(neurons_sel, 0, round(wake_ep.start.values[0]+length), wake_ep.start.values)
ephysplots.raster_basic(raster_list, dir2save)

