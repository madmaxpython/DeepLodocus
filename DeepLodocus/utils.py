
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 18:23:43 2022

@author: maximeteixeira
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy import sqrt as sqrt
import math
import matplotlib.image as mpimg
from matplotlib.widgets import PolygonSelector
from  shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import json

def TotalDistance(config, data_reduced, likelihood):
    temp_dist = []
    chunk_size=int(config['fps_camera']/4)
    prev_x_y=0
    for i in range(0,30000,chunk_size):
        chunk = data_reduced['Mouse 1']['spine1'][i:i+chunk_size]

        j=0
        while j < len(chunk):
            
            if likelihood[j+i][4] <0.8 :
                j+=1

            else: 
                if prev_x_y==0:
                    
                    prev_x_y = tuple(chunk.iloc[j])
                else: 
                    curr_x_y = tuple(chunk.iloc[j])
                    distance = sqrt((prev_x_y[0]-curr_x_y[0])**2 + (prev_x_y[1]-curr_x_y[1])**2)
                    if distance <200: 
                        temp_dist.append(distance*config['px_size'])
                    else:
                        temp_dist.append(0)
                    prev_x_y = curr_x_y 
                j+=chunk_size+1
                    
    tot_dist= np.nansum(temp_dist)
    return tot_dist


        
def TotalTime(config, areas, data_reduced,  likelihood, cage):
    time_zone={}
    entries_zone={}
    
    for f in config['zone_name']: #create a key in time & entries dict for each zone
        time_zone[f]=0
        entries_zone[f]=0
        
    
    chunk_size=int(config['fps_camera']/4)
    
    localization='' #variable of the localization (zone) of the animal

    for frame in range (0,30000, chunk_size):
        chunk = data_reduced['Mouse 1'][:][frame:frame+chunk_size] #take a chunk of the data 
        bodypart={}
        chunk_row=0 #Comptor through the chunk
        
        while chunk_row< len(chunk) and (frame+chunk_row<(len(data_reduced)-1)): #execute while not at the end of chunk or dataset
              
            it = iter(list(data_reduced.iloc[chunk_row+frame]))
            pata = [*zip(it, it)] #list of list of bodypart_coord
            
            for zone_name in config['zone_name']: #fill bodypart dict with bodypart as key and 0 as value
                bodypart[zone_name+'_bp']=0
            
            for bodypart_coord in pata:
                #print(frame+chunk_row, ' bodypart coordinate: ', pata , ' likelihood: ', likelihood[frame+chunk_row][pata.index(bodypart_coord)])
                for zone in config['zone_name']:
                    
                    
                    if areas['Cage'+cage+'_'+'Zone'+zone].contains(Point(bodypart_coord)) and (likelihood[frame+chunk_row][pata.index(bodypart_coord)]>0.8):
                        
                        bodypart[zone+'_bp']+=1
                        
                        if bodypart[zone+'_bp']==4:
                            time_zone[zone]+=1
                            if localization!=zone:
                                localization=zone
                                entries_zone[zone] += 1
                                
                    elif all(value == 0 for value in bodypart.values()) and chunk_row==len(chunk) and zone==config['zone_name'][-1] and bodypart_coord == pata[-1]:
                        localization=''
                    elif chunk_row< len(chunk):
                        chunk_row+=1
                        
            break
        
    for t in time_zone:
        time_zone[t]=time_zone[t]/4
    zone_dict={'time_zone': time_zone, 'entries_zone':entries_zone}
    return zone_dict
