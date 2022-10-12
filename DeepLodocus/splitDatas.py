#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import glob
import os
from pathlib import Path
from tkinter import Tk, filedialog

from utils import AreaSelector, tkAskString, FileSelector

SCRIPT_PATH = str(Path(__file__).parent)


class mouse:
    def __init__(self, data):
        self.data = data
        self.meanx = self.data.iloc[:, 0].mean()
        self.meany = self.data.iloc[:, 1].mean()
        self.point = Point(self.data.iloc[:, 0].mean(), self.data.iloc[:, 1].mean())
        self.WhoIsWho()

    def WhoIsWho(self):
        """
    self.point: point define by the mean coordinates of the mouse's nose
    Go through all the zone until self.point is in zone x
    When so, define self.identity as the mouse name associated with zone and save a csv with self.identity.csv as name
        """
        for x in range(1, NUMBER_OF_MICE + 1):
            if globals()[f"zone{x}"].contains(self.point):
                self.identity = MiceList[x - 1]
                self.data.to_csv(f"{SCRIPT_PATH}/ToSplit/Splitted/{self.identity}.csv")
                print(f'Mouse {x} is {MiceList[x - 1]}')
                break


if __name__ == '__main__':
    CSV_TO_TREAT = FileSelector('Select data to split', True, [("Tabular Datas", "*.csv")])
    print(CSV_TO_TREAT)

    for file in CSV_TO_TREAT:
        DATA = pd.read_csv(file, index_col=0)
        NUMBER_OF_MICE = int(len(DATA.columns)/27)
        for nb_columns in range(0, 27 * NUMBER_OF_MICE):
            DATA.iloc[0, nb_columns] = 'Mouse 1'

        DATA.columns = pd.MultiIndex.from_arrays(DATA.iloc[0:3].values)
        DATA = DATA.iloc[3:]
        DATA = DATA.astype(float)
        print("csv file to split: ", file)

        CALIBRATION_VIDEO = FileSelector('Select video', False, [("Video files", ".mp4 .MOV .avi")])[0]

        MiceList = []
        for zone_to_define in range(1, NUMBER_OF_MICE + 1):
            globals()[f"zone{zone_to_define}"] = Polygon(
                AreaSelector(f'Please, define cage of Mouse {zone_to_define}', CALIBRATION_VIDEO)
                                                        )
            MiceList.append(tkAskString('Select your cage', f'Mouse {zone_to_define} name'))

        print("List of mice: ", MiceList)

        for x in range(len(MiceList)):
            globals()[f"mouse{x + 1}"] = mouse(DATA.iloc[:, x * 27:(1 + x) * 27])
