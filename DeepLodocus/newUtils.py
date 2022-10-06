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
import cv2
import json


def TotalDistance(trackingData, likelihood, FPS, PIX_SIZE):
    """
    Measure the total distance travelled by the mice, using the 'spine1' label
    Parameters
    ----------
    config: use config to know the pixel_size and the fps of the video
    trackingData (np.array): tracking of the animal
    likelihood (np.array ): likelihood associate with tracking datas

    Returns: Total distance travelled
    -------
    """

    temp_dist = []
    chunk_size = int(FPS / 4)
    prev_x_y = 0
    for i in range(0, len(trackingData) - 10, chunk_size):
        chunk = trackingData[i:i + chunk_size]

        j = 0
        while j < len(chunk):

            if likelihood[j + i] < 0.8:
                j += 1

            else:
                if prev_x_y == 0:

                    prev_x_y = tuple(chunk.iloc[j])
                else:
                    curr_x_y = tuple(chunk.iloc[j])
                    distance = sqrt((prev_x_y[0] - curr_x_y[0]) ** 2 + (prev_x_y[1] - curr_x_y[1]) ** 2)
                    if distance < 200:
                        temp_dist.append(distance * PIX_SIZE)
                    else:
                        temp_dist.append(0)
                    prev_x_y = curr_x_y
                j += chunk_size + 1

    tot_dist = np.nansum(temp_dist)
    return tot_dist


def TotalTime(config, areas, trackingData, likelihood, cage):
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
                            likelihood[frame + chunk_row][current_BP.index(bodypart_coord)] > 0.8):

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


class askInput:
    def __init__(self, title, prompt, typeinput):
        self.root = Tk()
        self.root.title(title)
        self.typeinput = typeinput

        self.prompt = Label(self.root, text=prompt)
        self.prompt.grid(row=0, column=0)

        self.entry = Entry(self.root)
        self.entry.grid(row=1, column=0)

        self.button = Button(self.root, text='Enter', command=self.getEntry)
        self.button.grid(row=1, column=1)

        self.root.mainloop()

    def getEntry(self):
        try:
            value = self.convert(self.entry.get(), self.typeinput)
            self.root.quit()
            return value
        except:
            messagebox.showwarning('Error', f'Entry is not a {self.typeinput}')

    @staticmethod
    def convert(variable, typeasked):
        return typeasked(variable)

def FileSelector(TITLE, MULTIPLEFILES, FILETYPES):
    """
    Open a file dialog window to select files to transfer
    return: a list of files directory
    """
    selectwindow = Tk()
    selectwindow.withdraw()
    file_path = list(filedialog.askopenfilenames(title=TITLE, multiple=MULTIPLEFILES, filetypes=FILETYPES))
    selectwindow.destroy()

    return file_path

def FileSaver(TITLE, FILETYPES):
    saver = Tk()
    file_path = filedialog.asksaveasfilename(title=TITLE, filetypes=FILETYPES)
    saver.quit()
    return file_path

class AreaSelector:
    def __init__(self, VIDEO_PATH: str):
        self.VIDEO_PATH = VIDEO_PATH
        self.point = []

    def polyselector(self, TITLE_WINDOW):
        self.fig, self.ax = plt.subplots()
        self.ax.invert_yaxis()
        self.fig.canvas.manager.set_window_title('Calibration Step')

        self.video = cv2.VideoCapture(self.VIDEO_PATH)
        randomnb = random.randint(0, 300)
        self.video.set(1, randomnb)
        self.fig.suptitle(TITLE_WINDOW, fontsize=16)

        ret, frame = self.video.read()
        imgplot = plt.imshow(frame)
        self.lineprops = {'color': 'red', 'linewidth': 4, 'alpha': 0.8}
        self.point = PolygonSelector(ax=self.ax, onselect=self.onClick, lineprops=self.lineprops)
        plt.show()

        return self.point

    def onClick(self, event):
        self.point=event
        plt.close("all")
        return self.point



class dictSerializer:
    @staticmethod
    def saveJSON(config, path):
        strconfig = json.dumps(config)
        with open(path, 'w') as file:
            file.write(strconfig)

    @staticmethod
    def loadJSON(path):
        with open(path, "r") as dictonary:
            dictonary = json.loads(dictonary.read())
        return dictonary
