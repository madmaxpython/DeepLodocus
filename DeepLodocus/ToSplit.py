#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import glob, os
from pathlib import Path

script_path = str(Path(__file__).parent)
zone1 = Polygon([[0, 730], [386, 730], [386, 365], [0, 365]])
zone2 = Polygon([[386, 730], [772, 730], [772, 365], [386, 365]])
zone3 = Polygon([[0, 0], [0, 365], [386, 365], [386, 0]])
zone4 = Polygon([[386, 0], [772, 0], [772, 365], [386, 365]])

class mouse():
    def __init__(self, data):
        self.data=data
        self.meanx=self.data.iloc[:,0].mean()
        self.meany=self.data.iloc[:,1].mean()
        self.point= Point(self.data.iloc[:,0].mean(), self.data.iloc[:,1].mean())
        
    def who(self):
        for x in range(1,5):
            if globals()[f"zone{x}"].contains(self.point):
                self.identity=name[x-1]
                print(self, ' is ', self.identity)
                self.data.to_csv('/ToSplit/Splitted/'+self.identity+'.csv')
                
                
                
                
         
for file in glob.glob(os.path.join(script_path,'ToSplit', "*.csv")):
    name=[]
    
    data = pd.read_csv(file, index_col=0,)
    for x in range (0, 108):
        data.iloc[0, x]= 'Mouse 1'
    
    
    data.columns=pd.MultiIndex.from_arrays(data.iloc[0:3].values)
    
    data=data.iloc[3:]
    data= data.astype(float)
    print("File: ", file)
    
    name.append(str(input("Mouse 1 (Top-left corner): ")))
    name.append(str(input("Mouse 2 (Top-right corner): ")))
    name.append(str(input("Mouse 3 (Bottom-left corner): ")))
    name.append(str(input("Mouse 4 (Bottom-right corner): ")))
    
    print("Mice to treat (in order): ", name)
    mouse1= mouse(data.iloc[:, 0:27])
    mouse1.who()
    mouse2= mouse(data.iloc[:, 27:54])
    mouse2.who()
    mouse3= mouse(data.iloc[:, 54:81])
    mouse3.who()
    mouse4= mouse(data.iloc[:, 81:108])
    mouse4.who()
    



        
