#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 16:40:02 2022

@author: maximeteixeira
"""
import os, glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy import sqrt as sqrt
import math
import matplotlib.image as mpimg
from matplotlib.widgets import PolygonSelector
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import json
from pathlib import Path
import random
import cv2


SCRIPT_PATH = str(Path(__file__).parent)

with open(SCRIPT_PATH+"/config.txt", "r") as config_file:
    config = json.loads(config_file.read())
    
os.chdir(SCRIPT_PATH+"/Datas")

VIDEO_TO_TREAT=[]
for file in glob.glob("*.mp4"):
    VIDEO_TO_TREAT.append(file)
    
def AreaSelector(zone_nb,cage,config, element):
    fig, ax = plt.subplots()
    ax.invert_yaxis()
    fig.canvas.manager.set_window_title('Calibration Step')
    fig.suptitle('Please, define Zone '+str(config['zone_name'][zone_nb])+' for cage'+str(cage), fontsize=16)
    
    cap = cv2.VideoCapture("/Users/maximeteixeira/Desktop/DeepLodocus/Datas/"+element)
    randomnb=random.randint(0,30000)
    cap.set(1, randomnb)
    
    ret, frame = cap.read()
    imgplot = plt.imshow(frame)
    
    lineprops = {'color': 'red', 'linewidth': 4, 'alpha': 0.8}
    lsso = PolygonSelector(ax=ax, onselect=onSelect, lineprops=lineprops)
    plt.show()
    return coord

def onSelect(x):
    global coord
    if len(x) != 0:
        plt.close()
    coord = x
    return coord

def zone_file(config, VIDEO_TO_TREAT):
    areas_list={}

    for cage in range (1,config['nb_cage']+1):
        current_cage=[]
        for element in VIDEO_TO_TREAT:
            if element[0]==str(cage):
                current_cage.append(element)
        
        if current_cage!=[]:
            for calibration in range(len(config['zone_name'])):
                areas_list["Cage"+str(cage)+"_"+"Zone"+str(config['zone_name'][calibration])]=AreaSelector(calibration,cage,config, current_cage[0])

    areas_list = json.dumps(areas_list)

    zone_file = open(SCRIPT_PATH+"/zone.txt", "w")
    zone_file.write(str(areas_list))
    zone_file.close()

if __name__ == "__main__":
    zone_file(config, VIDEO_TO_TREAT)


