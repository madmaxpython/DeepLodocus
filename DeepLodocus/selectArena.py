#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 matplotlib-3.3.2
Created on Mon Apr 25 16:40:02 2022

@author: maximeteixeira
"""
import glob
import yaml
import os
from Utils import AreaSelector, YamlConfig
import numpy as np


def ZoneSelector(config, VIDEO_PATH, VIDEO_TO_TREAT):
    areas_list = {}
    for element in VIDEO_TO_TREAT:
        areas_list[f"Cage{element[0]}"] = {}
        # video = AreaSelector(f"{SCRIPT_PATH}/Datas/{element}")
        for calibration in config['ZONE']['zone_name']:
            areas_list[f"Cage{element[0]}"][calibration] = AreaSelector(
                os.path.join(VIDEO_PATH, element)).polygon_selector(
                f"Please, define Zone {calibration} for cage {element[0]}")
    return areas_list


def represent_scalar(dumper, data):
    if isinstance(data, np.float64):
        return dumper.represent_float(float(data))
    return dumper.represent_scalar('tag:yaml.org,2002:str', str(data))


def represent_array(dumper, data):
    return dumper.represent_sequence('tag:yaml.org,2002:seq', data.tolist())


def represent_ndarray(dumper, data):
    return represent_array(dumper, data.flatten())


def represent_tuple(dumper, data):
    return dumper.represent_sequence('tag:yaml.org,2002:seq', list(data))


yaml.add_representer(np.ndarray, represent_ndarray)
yaml.add_representer(np.float64, represent_scalar)
yaml.add_representer(tuple, represent_tuple)


def Arena_selector(VIDEO_PATH, VIDEO_EXTENSION, CONFIG_PATH):

    config_yaml = YamlConfig(CONFIG_PATH)
    config = config_yaml.load()

    video_to_treat = []
    for file in glob.glob(os.path.join(VIDEO_PATH, f"*{VIDEO_EXTENSION}")):
        video_to_treat.append(file.split("/")[-1])
    video_to_treat = sorted(video_to_treat)

    sample_files = list()

    for file_name in video_to_treat:
        file_number = file_name[0]
        if file_number not in sample_files:
            example_file = next(file for file in video_to_treat if file.startswith(file_number))
            sample_files.append(example_file)

    area_coord = ZoneSelector(config, VIDEO_PATH, sample_files)

    config['ZONE'] = {'zone_name': config['ZONE']['zone_name']}

    config['ZONE'].update(area_coord)

    config_yaml.save(config)
