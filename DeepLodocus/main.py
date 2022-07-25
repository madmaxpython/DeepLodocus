#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 10:39:14 2022

@author: maximeteixeira
"""

import glob, os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy import sqrt as sqrt
import math
import matplotlib.image as mpimg
from matplotlib.widgets import PolygonSelector
import utils as analysis
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import json
from pathlib import Path

script_path = str(Path(__file__).parent)

# Import config dictionnary from a .txt file
with open(script_path+'/config.txt', "r") as config_file:
    config = json.loads(config_file.read())


config['path_env']=script_path

class Mouse ():
    num_of_mice=0
    
    def __init__(self, csvname):
        self.csvname = csvname
        self.cage=csvname[0]
        self.name = csvname.split('_')[1].split('.')[0]
        self.data = pd.read_csv(config['path_env']+'/Datas/'+self.csvname,header=[1,2,3], index_col=0)
        self.likelihood = np.array(self.data.loc[:, [x for x in self.data.columns.values if 'likelihood'  in str(x)]])
        #Create a dataframe without likelihood columns
        columns_to_use = [x for x in self.data.columns.values if 'likelihood' not in str(x)]
        self.data_reduced = self.data.loc[:,columns_to_use]  
        
        Mouse.num_of_mice+=1
        
    def analyze_zone(self):
        with open(config['path_env']+"/zone.txt", "r") as zone_file:
            areas = json.loads(zone_file.read())

        for zone in areas:
            areas[zone]=Polygon(areas[zone])
        
        
        output_zone = analysis.TotalTime(config, areas, self.data_reduced, self.likelihood, self.cage)
        
        self.time_zone=output_zone['time_zone']
        self.entries_zone = output_zone['entries_zone']
    
        
    def analyze_distance(self):
        self.distance_travelled=analysis.TotalDistance(config, self.data_reduced, self.likelihood)
        

df_analysis=pd.DataFrame()

#Look for csv files, and create an instance Mouse for each of them
for file in glob.glob(os.path.join(config['path_env'],'Datas', "*.csv")):
    mouse_id = glob.glob(os.path.join(config['path_env'],'Datas', "*.csv")).index(file)
    globals()[f"mouse_{mouse_id}"]=Mouse(file.split("Datas/",1)[1])
    df_analysis[globals()[f"mouse_{mouse_id}"].name]=0
        


#If time or entries in zones need to be analyze, create a list for each of them
if config['analyse_zone']==True or config['analyse_entries']==True:
    for zonee in config['zone_name']:
        globals()[f"list_time_{zonee}"]= []
        globals()[f"list_entries_{zonee}"]= []
     
#If distance travelled need to be analyze, create a list        
if config['analyse_distance']==True:
     list_distance=[]

#For each measure, fill a list of this measure for all the mice 
for mice_nb in range (Mouse.num_of_mice):    
    if config['analyse_zone']==True or config['analyse_entries']==True:
        
        globals()[f"mouse_{mice_nb}"].analyze_zone()
        
        for zone in config['zone_name']:
            
            if config['analyse_zone']==True:
                globals()[f"list_time_{zone}"].append(globals()[f"mouse_{mice_nb}"].time_zone[zone])

            if config['analyse_entries']==True:
                globals()[f"list_entries_{zone}"].append(globals()[f"mouse_{mice_nb}"].entries_zone[zone])

            if mice_nb == Mouse.num_of_mice-1: #If it is the last mouse, create a row in dataframe made of the list of this measure
                if config['analyse_zone']==True:
                    df_analysis.loc['Time in zone '+zone+' (sec)']=globals()[f"list_time_{zone}"]
                    
                if config['analyse_entries']==True: #If it is the last mouse, create a row in dataframe made of the list of this measure
                    df_analysis.loc['Entries in '+zone]=globals()[f"list_entries_{zone}"]

                
    if config['analyse_distance']==True:
        globals()[f"mouse_{mice_nb}"].analyze_distance()
        list_distance.append(globals()[f"mouse_{mice_nb}"].distance_travelled)
        
        if mice_nb == Mouse.num_of_mice-1:
            df_analysis.loc['Distance travelled (cm)']=list_distance
        
        
    
print('\n \nData CPP Video __________________________________________________\n', df_analysis)
df_analysis.to_excel(config['path_env'] +'/Output/'+str(Mouse.num_of_mice)+ config['output_excel'])


        
    