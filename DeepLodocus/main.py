import pandas as pd
import numpy as np
import os
from pathlib import Path
from DeepLodocus.Utils import total_time, total_distance, DictSerializer
import cv2


class Experiment:
    deeplodocus_path = str(Path(__file__).parent)
    animal_list = []

    def __init__(
            self,
            path_experiment: str,
            likelihood_threshold: float = 0.9,
            iterative_imputer: bool = True,
            table_format: str = '.csvfiles',
            video_format: str = ".mp4"
            ):

        ### CREATE USEFUL PATH STRING + LIST OF CSV & VIDEOS ###
        self.path_experiment = path_experiment

        self.path_csv = f'{path_experiment}/csvfiles/'
        self.table_format = table_format
        self.list_csv = sorted([os.path.join(self.path_csv, i) for i in os.listdir(self.path_csv)
                                if not i.startswith(".") and i.endswith(self.table_format)])

        self.path_videos = f'{path_experiment}/videos/'
        self.video_format = video_format
        self.list_video = sorted([os.path.join(self.path_videos, i) for i in os.listdir(self.path_videos)
                                  if not i.startswith(".") and i.endswith(self.video_format)])

        try:
            len(self.list_csv) == len(self.list_video)
        except:
            print(f"Different number of tabular (n={len(self.list_csv)} files and videos (n={len(self.list_video)}")

        ### ###

        self.enable_iterative_imputer = iterative_imputer

        Animal.likelihood_threshold = likelihood_threshold

    @property
    def config(self):
        config = DictSerializer.loadJSON(self.deeplodocus_path + '/config.txt')
        config['fps_camera'] = cv2.VideoCapture(self.list_video[0]).get(cv2.CAP_PROP_FPS)
        return config

    def load_animal(self, animal_model):
        for csv in self.list_csv:
            animal_model(csv)

        if self.enable_iterative_imputer:
            from DeepLodocus.Utils import it_imputer

            for animal in self.animal_list:
                animal.tracking_data = it_imputer(animal.tracking_data)

    def analyze(self,
                distance: bool = False,
                time_zone: bool = False,
                entries_zone: bool = False,
                output_file_name: str = None
                ):

        areas_dict = DictSerializer.loadJSON(self.deeplodocus_path + "/zone.txt")

        ## Create the empty dataframe_output ###
        columns = {"Animal ID": []}
        if distance:
            columns["Distance"] = []
        if time_zone:
            for zone in self.config["zone_name"].values:
                columns[f"Time in {zone}"] = []

        if entries_zone:
            for zone in self.config["zone_name"].values:
                columns[f"Entries in {zone}"] = []

        dataframe_output = pd.DataFrame(columns)
        ####

        for animal in self.animal_list:

            measurement = [animal.name]

            if distance:
                measurement.append(total_distance(animal.tracking_data[:, 6:8],
                                                  animal.likelihood[:, 3],
                                                  self.config['fps_camera'],
                                                  self.config['px_size']
                                                  )
                                   )

            if time_zone or entries_zone:
                time_zone, entries_zone = total_time(self.config,
                                                     areas_dict,
                                                     animal.tracking_data,
                                                     animal.likelihood,
                                                     animal.cage,
                                                     animal.body_part_nb
                                                     )

                if time_zone:
                    measurement.append(time_zone)

                if entries_zone:
                    measurement.append(entries_zone)

            dataframe_output.loc[len(dataframe_output)] = measurement

        print('\n \nDatas __________________________________________________\n', dataframe_output)

        if output_file_name is None:
            output_file_name = 'Analyzed_Datas'

        return dataframe_output.to_csv(os.path.join(self.path_experiment, f'{output_file_name}.csvfiles'))


class Animal:
    likelihood_threshold = 0.9
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

    def __init__(self, data_path):
        self.name = data_path.split('_')[1].split('.')[0]
        self.cage = data_path[0]

        self.data = pd.read_csv(data_path, header=[2, 3], index_col=0)

        self.likelihood = np.array(self.data.loc[:, [x for x in self.data.columns.values if
                                                     'likelihood' in str(x)]],
                                   dtype='float16') > self.likelihood_threshold

        self.tracking_data = np.array(self.data.loc[:, [x for x in self.data.columns.values if not
        'likelihood' in str(x)]], dtype='float32')


class Mouse(Animal):
    """
    Child of Animal class for Mouse
    """
    numMouse = 0
    body_part_nb = 9
    head = ['nose', 'leftear', 'rightear']
    body = ['spine1', 'spine2', 'spine3']
    tail = ['tailbase', 'tailmid', 'tailend']
    body_parts = list(head + body + tail)
    body_sections = {'head': head, 'body': body, 'tail': tail}

    def __init__(self, data_path):
        super().__init__(data_path)
        Mouse.numMouse += 1
        Experiment.animal_list.append(self)
