#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 00:58:36 2021

@author: vite
"""

from dearpygui.core import *
from dearpygui.simple import *
from os import system
from load_data_forgui import *

set_main_window_size(940, 1020)
set_global_font_scale(1.5)
set_theme("Gold")
set_style_window_padding(30,30)

food = []
def getpath(sender, data):
    food.append(get_value("path"))
    with window("Tetractys"):
        add_separator()
        add_spacing(count=12)
        add_text("you are doing well")
    
def getepisodes(sender, data):
    food.append(get_value("episodes").split(","))
    with window("Tetractys"):
        hide_item("you are doing well")
        add_text("almost there")

def gendata(sender, data):
    with window("Tetractys"):
        hide_item("almost there")
        add_text("Below the thunders of the upper brain-deep, \nFar, far beneath in the abysmal sea, \nHis ancient, dreamless, uninvaded SWS and REM sleep \nThe Kraken sleepeth: faintest sunlights flee...")
    awake(food[0], food[1])
# def sel_dir(sender, data):
#     select_directory_dialog(callback=apply_selected_directory)

# def apply_selected_directory(sender, data):
#     log_debug(data)  # so we can see what is inside of data
#     directory = data[0]
#     folder = data[1]
#     set_value("directory", directory)
#     set_value("folder", folder)
#     set_value("folder_path", f"{directory}\\{folder}")
    
with window("Tetractys"): # with is for parents  
    add_drawing("kraken", width = 740, height=450)
    add_spacing(count=12)
    add_separator()
    add_spacing(count=12)
    add_input_text(name = "path", on_enter = True, callback = getpath, hint = "/")

    # add_button(name = "folder", callback=sel_dir)
    # add_text("Folder Path: ")
    # add_same_line()
    # add_label_text("##folderpath", source="folder_path", color=[255, 0, 0])
    add_spacing(count=12)
    add_input_text(name = "episodes", on_enter = True, callback = getepisodes, hint = "e.g. wake, sleep, wake")
    add_spacing(count=12)
    add_button("Now dare to awake the Kraken", callback = gendata)
    add_spacing(count=12)
draw_image("kraken", "kraken.jpg", [650, 0], [50, 450])
start_dearpygui()


"""

def directory_picker(sender, data):
    select_directory_dialog(callback=apply_selected_directory)

def apply_selected_directory(sender, data):
    log_debug(data)  # so we can see what is inside of data
    directory = data[0]
    folder = data[1]
    set_value("directory", directory)
    set_value("folder", folder)

show_logger()

with window("Tutorial"):
    add_button("Directory Selector", callback=directory_picker)
    add_text("Directory Path: ")
    add_same_line()
    add_label_text("##dir", source="directory", color=[255, 0, 0])
    add_text("Folder: ")
    add_same_line()
    add_label_text("##folder", source="folder", color=[255, 0, 0])
    add_text("Folder Path: ")
    add_same_line()
    add_label_text("##folderpath", source="folder_path", color=[255, 0, 0])

start_dearpygui()
"""