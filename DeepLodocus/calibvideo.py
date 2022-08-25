#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 16:40:02 2022

@author: maximeteixeira
"""
import glob
import json
import os

from pathlib import Path
from utils import AreaSelector

SCRIPT_PATH = str(Path(__file__).parent)

with open(SCRIPT_PATH + "/config.txt", "r") as config_file:
    config = json.loads(config_file.read())

os.chdir(SCRIPT_PATH + "/Datas")

VIDEO_TO_TREAT = []
for file in glob.glob("*.mp4"):
    VIDEO_TO_TREAT.append(file)


def zone_file(config, VIDEO_TO_TREAT):
    areas_list = {}

    for cage in range(1, 20):
        current_cage = []
        for element in VIDEO_TO_TREAT:
            if element[0] == str(cage):
                current_cage.append(element)

        if current_cage:
            for calibration in range(len(config['zone_name'])):
                areas_list[f"Cage {cage}_Zone{config['zone_name'][calibration]}"] = AreaSelector(
                    f"Please, define Zone {config['zone_name'][calibration]} for cage {cage}",
                    f"{SCRIPT_PATH}/Datas/{element}")

    areas_list = json.dumps(areas_list)

    zone_file = open(SCRIPT_PATH + "/zone.txt", "w")
    zone_file.write(str(areas_list))
    zone_file.close()


if __name__ == "__main__":
    zone_file(config, VIDEO_TO_TREAT)
