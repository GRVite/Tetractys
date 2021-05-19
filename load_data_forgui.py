#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 21:05:49 2021

@author: vite
"""
from functions import *
from my_functions import *
from wrappers import *
import pandas as pd
import pickle
import os
from shutil import copyfile
import numpy as np

def awake(data_directory, episodes):
    # Load the spikes and shank data

    #copy XML
    # copyfile(data_directory + '/' + session + '.xml', OneD + '/' + session + '.xml')
    # data_directory = '/Volumes/LaCiel/Timaios/Kilosorted/A4403/A4403-200626/A4403-200626'
    spikes, shank = loadSpikeData(data_directory)
    
    # Find the number of events
    events = []
    for i in os.listdir(data_directory):
        if os.path.splitext(i)[1]=='.csv':
            if i.split('_')[1][0] != 'T': 
                events.append( i.split('_')[1][0])
    events.sort()
    
    
    # Load the position of the animal derived from the camera tracking
    position = loadPosition(data_directory, events, episodes)
    
    
    #create a new directory for saving the data
    os.mkdir(data_directory + '/my_data')
    
    # Get the time interval of the wake epoch
    wake_ep = loadEpoch(data_directory, 'wake', episodes)
    if 'sleep' in episodes:
        sleep_ep = loadEpoch(data_directory, 'sleep')
        with open(data_directory + '/my_data/' + 'sleep_ep' + '.pickle', 'wb') as handle:
            pickle.dump(sleep_ep, handle, protocol=pickle.HIGHEST_PROTOCOL)
            
    #save data in pickle format
    
    for string, objct in zip(['spikes', 'shank', 'episodes', 'position', \
                  'wake_ep'],
                  [spikes, shank, episodes, position, wake_ep]):
        with open(data_directory + '/my_data/' + string + '.pickle', 'wb') as handle:
            pickle.dump(objct, handle, protocol=pickle.HIGHEST_PROTOCOL)