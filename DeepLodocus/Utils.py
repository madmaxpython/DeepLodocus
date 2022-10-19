#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 18:23:43 2022

@author: maximeteixeira
"""

import numpy as np
import matplotlib.pyplot as plt
from numpy import sqrt as sqrt
import random
from matplotlib.widgets import PolygonSelector
from shapely.geometry import Point
from tkinter import *
from tkinter import messagebox, filedialog
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
import cv2
import json


def total_distance(trackingData, likelihood, FPS, PIX_SIZE):
    """
    Measure the total distance travelled by the mice, using the 'spine1' label
    Parameters
    ----------
    FPS: FPS of the original video
    PIX_SIZE: size in cm of a pixel
    trackingData: (np.array): tracking of the animal
    likelihood: (np.array ): likelihood associate with tracking datas

    Return:
    -------
    tot_dist: Total distance travelled
    """

    temp_dist = []
    chunk_size = int(FPS / 4)
    prev_x_y = 0

    for i in range(0, len(trackingData) - 10, chunk_size):
        chunk = trackingData[i:i + chunk_size]

        j = 0
        while j < len(chunk):

            if likelihood[j + i]:
                j += 1

            else:
                if prev_x_y == 0:

                    prev_x_y = tuple(chunk[j])
                else:
                    curr_x_y = tuple(chunk[j])
                    distance = sqrt((prev_x_y[0] - curr_x_y[0]) ** 2 + (prev_x_y[1] - curr_x_y[1]) ** 2)
                    if distance < 200:
                        temp_dist.append(distance * PIX_SIZE)
                    else:
                        temp_dist.append(0)
                    prev_x_y = curr_x_y
                j += chunk_size + 1
    std_dev = np.std(temp_dist)
    tot_dist = np.nansum(temp_dist)
    return tot_dist


def total_time(config, areas, trackingData, likelihood, cage, bodypart_nb):
    time_zone = {}
    entries_zone = {}

    for allzone in config['zone_name']:  # create a key in time & entries dict for each zone
        time_zone[allzone] = 0
        entries_zone[allzone] = 0

    chunk_size = int(config['fps_camera'] / 4)

    localization = ''  # variable of the localization (zone) of the animal

    for frame in range(0, len(trackingData) - 10, chunk_size):
        chunk = trackingData[frame:frame + chunk_size]  # take a chunk of the data
        bodypart = {}
        chunk_row = 0  # Counter through the chunk

        while chunk_row < len(chunk) and (
                frame + chunk_row < (len(trackingData) - 1)):  # execute while not at the end of chunk or dataset

            it = iter(list(trackingData.iloc[chunk_row + frame]))
            current_BP = [*zip(it, it)]  # list of list of bodypart_coord

            for zone_name in config['zone_name']:  # fill bodypart dict with bodypart as key and 0 as value
                bodypart[zone_name + '_bp'] = 0

            for bodypart_coord in current_BP:
                # print(frame+chunk_row, ' bodypart coordinate: ', current_BP , ' likelihood: ', likelihood[
                # frame+chunk_row][current_BP.index(bodypart_coord)])
                for zone in config['zone_name']:

                    if areas['Cage' + cage + '_' + 'Zone' + zone].contains(Point(bodypart_coord)) and (
                            likelihood[frame + chunk_row][current_BP.index(bodypart_coord)]):

                        bodypart[zone + '_bp'] += 1

                        if bodypart[zone + '_bp'] == 4:
                            time_zone[zone] += 1
                            if localization != zone:
                                localization = zone
                                entries_zone[zone] += 1

                    elif all(value == 0 for value in bodypart.values()) and chunk_row == len(chunk) and zone == \
                            config['zone_name'][-1] and bodypart_coord == current_BP[-1]:
                        localization = ''
                    elif chunk_row < len(chunk):
                        chunk_row += 1

            break

    for t in time_zone:
        time_zone[t] = time_zone[t] / 4
    zone_dict = {'time_zone': time_zone, 'entries_zone': entries_zone}
    return zone_dict


class AskInput:
    def __init__(self, title, prompt, typeinput):
        self.root = Tk()
        self.root.title(title)
        self.type_input = typeinput

        self.prompt = Label(self.root, text=prompt)
        self.prompt.grid(row=0, column=0)

        self.entry = Entry(self.root)
        self.entry.grid(row=1, column=0)

        self.button = Button(self.root, text='Enter', command=self.get_entry)
        self.button.grid(row=1, column=1)

        self.root.mainloop()

    def get_entry(self):
        try:
            value = self.convert(self.entry.get(), self.type_input)
            self.root.quit()
            return value
        except:
            messagebox.showwarning('Error', f'Entry is not a {self.type_input}')

    @staticmethod
    def convert(variable, type_asked):
        return type_asked(variable)


def file_selector(TITLE, MULTIPLE_FILES, FILETYPES):
    """
    Open a file dialog window to select files to transfer
    return: a list of files directory
    """
    selectwindow = Tk()
    selectwindow.withdraw()
    file_path = list(filedialog.askopenfilenames(title=TITLE, multiple=MULTIPLE_FILES, filetypes=FILETYPES))
    selectwindow.destroy()

    return file_path


def file_saver(TITLE, FILETYPES):
    saver = Tk()
    file_path = filedialog.asksaveasfilename(title=TITLE, filetypes=FILETYPES)
    saver.quit()
    return file_path


class AreaSelector:
    def __init__(self, VIDEO_PATH: str):
        self.VIDEO_PATH = VIDEO_PATH
        self.lineprops = {'color': 'red', 'linewidth': 4, 'alpha': 0.8}
        self.point = []

    def polygon_selector(self, TITLE_WINDOW):
        self.fig, self.ax = plt.subplots()
        self.ax.invert_yaxis()
        self.fig.canvas.manager.set_window_title('Calibration Step')

        self.video = cv2.VideoCapture(self.VIDEO_PATH)
        random_nb = random.randint(0, 300)
        self.video.set(1, random_nb)
        self.fig.suptitle(TITLE_WINDOW, fontsize=16)

        ret, frame = self.video.read()
        image_plot = plt.imshow(frame)
        self.point = PolygonSelector(ax=self.ax, onselect=self.onClick, lineprops=self.lineprops)
        plt.show()

        return self.point

    def onClick(self, event):
        self.point = event
        plt.close("all")
        return self.point


class DictSerializer:
    @staticmethod
    def saveJSON(config, path):
        str_config = json.dumps(config)
        with open(path, 'w') as file:
            file.write(str_config)

    @staticmethod
    def loadJSON(path):
        with open(path, "r") as dictionary:
            dictionary = json.loads(dictionary.read())
        return dictionary


def it_imputer(data):
    imput_it = IterativeImputer(missing_values=np.nan, tol=0.001, max_iter=10)
    return imput_it.fit_transform(data)
