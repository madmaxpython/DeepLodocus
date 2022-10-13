#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import numpy as np
from pathlib import Path
from tkinter import Tk, filedialog

from newUtils import AreaSelector, AskInput, file_selector

SCRIPT_PATH = str(Path(__file__).parent)


class mouse:
    NB_MICE=0
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.mean_x = np.mean(np.array([x for x in self.data.iloc[3:, 0] if 'nan' not in str(x)], dtype='float16'))
        self.mean_y = np.mean(np.array([x for x in self.data.iloc[3:, 1] if 'nan' not in str(x)], dtype='float16'))
        self.point = Point(self.mean_x, self.mean_y)
        self.WhoIsWho()

    def WhoIsWho(self):
        """
    self.point: point define by the mean coordinates of the mouse's nose
    Go through all the zone until self.point is in zone x
    When so, define self.identity as the mouse name associated with zone and save a csv with self.identity.csv as name
        """
        for x in range(1, NB_MICE + 1):
            if globals()[f"zone{x}"].contains(self.point):
                self.identity = MiceList[x - 1]
                self.data.to_csv(f"{SCRIPT_PATH}/ToSplit/Splitted/{self.identity}.csv")
                print(f'Mouse {x} is {MiceList[x - 1]}')
                break


if __name__ == '__main__':
    CSV_TO_TREAT = file_selector('Select data to split', True, [("Tabular file", "*.csv")])
    print(CSV_TO_TREAT)

    for file in CSV_TO_TREAT:
        DATA = pd.read_csv(file, index_col=0)
        NB_BP = 9
        mouse.NB_MICE = int(len(DATA.columns)/(9*3))

        print("csv file to split: ", file)

        CALIBRATION_VIDEO = file_selector('Select video', False, [("Video files", ".mp4 .MOV .avi")])[0]

        MiceList = []
        for zone_to_define in range(1, mouse.NB_MICE + 1):
            globals()[f"zone{zone_to_define}"] = Polygon(
                AreaSelector(CALIBRATION_VIDEO).polygon_selector(f'Please, define cage of Mouse {zone_to_define}')
                                                        )
            MiceList.append(AskInput('Select your cage', f'Mouse {zone_to_define} name', str).get_entry())

        print("List of mice: ", MiceList)

        for x in range(len(MiceList)):
            globals()[f"mouse{x + 1}"] = mouse(DATA.iloc[:, x * 27:(1 + x) * 27])
