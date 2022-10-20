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

def read_dlc_input(path_to_file):
    tracks_dictionary = {}
    #likelihood_dictionary = {}
    data = pd.read_csv(path_to_file, header=[2,3], index_col=0)
    bodyparts = list(data.columns.levels[0])

    for bodypart in bodyparts:
        #np.array(data[bodypart][['x','y']]) # do we want this for track processing?
        tracks_dictionary[bodypart] = np.array(data[bodypart][['x','y']],dtype='float32',)
        #likelihood_dictionary[bodypart] = np.array(data[bodypart][['likelihood']],dtype='float32')

    return tracks_dictionary
