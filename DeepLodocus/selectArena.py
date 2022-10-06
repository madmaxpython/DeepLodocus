#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 matplotlib-3.3.2
Created on Mon Apr 25 16:40:02 2022

@author: maximeteixeira
"""
import glob
import json
import os
from pathlib import Path
from newUtils import AreaSelector, dictSerializer

SCRIPT_PATH = str(Path(__file__).parent)

config = dictSerializer.loadJSON(SCRIPT_PATH + '/config.txt')

VIDEO_TO_TREAT = []
for file in glob.glob(os.path.join(SCRIPT_PATH, 'Datas', "*.mp4")):
    VIDEO_TO_TREAT.append(file.split("/")[-1])

VIDEO_TO_TREAT = sorted(VIDEO_TO_TREAT)


def ZoneSelector(config, VIDEO_TO_TREAT):
    areas_list = {}

    for element in VIDEO_TO_TREAT:
        video = AreaSelector(f"{SCRIPT_PATH}/Datas/{element}")
        for calibration in range(len(config['zone_name'])):
            areas_list[f"Cage{element[0]}_Zone{config['zone_name'][calibration]}"] = video.polyselector(
                f"Please, define Zone {config['zone_name'][calibration]} for cage {element[0]}")


    dictSerializer.saveJSON(areas_list, SCRIPT_PATH + '/zone.txt')


if __name__ == "__main__":
    ZoneSelector(config, VIDEO_TO_TREAT)
