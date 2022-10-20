import os
import re
import random # if we want to do bootstrapping
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from pathlib import Path
import DeepLodocus.DeepLodocus.newnewUtils as DeepL_utils
import cv2


class Experiment():

    def __init__(
            self,
            path: str = os.getcwd(), # set it to '.../DeepLodocus-NewMaster/DeepLodocus/DeepLodocus'
            animal_model: str = 'Mouse',
            animal_list: list = [],
            likelihood_threshold: float = 0.9,
            enable_iterative_imputer: bool = True,
            table_format: str = 'csv',
            video_format: str = 'mp4'
    ):

        self.path = path
        self.csv_path = os.path.join(self.path, 'Data/csvfiles')
        self.table_format = table_format
        self.csv_files = sorted([csvfile for csvfile in os.listdir(self.csv_path)
                                 if csvfile.endswith(self.table_format) and not csvfile.startswith(".")])
        self.animal_ids = sorted([animal_id.split('.csv')[0] for animal_id in self.csv_files])

        #self.video_path = os.path.join(self.path, 'videos')
        #self.video_format = video_format
        #self.video_files = sorted([os.path.join(self.video_path, video) for video in os.listdir(self.video_path)
        #                          if not video.startswith(".") and video.endswith(self.video_format)])

        #assert len(self.list_csv) == len(self.list_video), \
        #    f"Different number of tabular (n={len(self.list_csv)} files and videos (n={len(self.list_video)}"

        self.animal_model = animal_model
        self.animal_list = animal_list
        self.enable_iterative_imputer = enable_iterative_imputer

        print(f'You created a self-contained object with {self.animal_model} data')

        #Animal.likelihood_threshold = likelihood_threshold

    #@property
    #def config(self):
    #    config = DictSerializer.loadJSON(self.deeplodocus_path + '/config.txt')
    #    config['fps_camera'] = cv2.VideoCapture(self.list_video[0]).get(cv2.CAP_PROP_FPS)
    #    return config

    def load_animals(self, animal_model):

        for animal_id, csvfile in enumerate(self.csv_files):
            curr_animal = None
            exec(f'curr_animal = {animal_model}(os.path.join(self.csv_path,csvfile))')
            self.animal_list.append(curr_animal)


            #self.coordinates_data = DeepL_utils.read_dlc_input(os.path.join(self.csv_path, csvfile))
            #tracks_dictionary[self.animal_ids[animal_id]] = pd.read_csv(os.path.join(self.csv_path,csvfile))

class Animal:

    """
    Create an animal from a tabular file using info in the name.
    (Created if we want to add new animal models to DeepLodocus)
    Args:
        data_path (str): path of the tabular file
    self:
        name (str) : experimental name of the animal
        cage (str) : cage associate with a camera where Animal behaved
        data (pd.Dataframe) : DeepLabCut output tracking data
    """



    def __init__(self,
                 path: str = os.getcwd()):
        self.path = path
        self.csv_path = os.path.join(self.path, 'Data/csvfiles')
        self.csv_files = sorted([csvfile for csvfile in os.listdir(self.csv_path)
                                 if csvfile.endswith(self.table_format) and not csvfile.startswith(".")])
        self.animal_ids = sorted([animal_id.split('.csv')[0] for animal_id in self.csv_files])
        #self.name =


        #self.cage = data_path[0]

        #self.data = pd.read_csv(data_path, header=[2, 3], index_col=0)

        #self.likelihood = np.array(self.data.loc[:, [x for x in self.data.columns.values if
        #                    'likelihood' in str(x)]], dtype='float16') > self.likelihood_threshold

        #self.tracking_data = np.array(self.data.loc[:, [x for x in self.data.columns.values if not
        #                        'likelihood' in str(x)]], dtype='float32')


class Mouse(Animal):
    """
    Child of Animal class for Mouse
    """

    print("Hello...this is a mouse :)")

    def __init__(self,):
        super().__init__()
        print('thank you for your service')