import pandas as pd
import numpy as np
import os
from pathlib import Path
from DeepLodocus.newUtils import total_time, total_distance, DictSerializer
import cv2


class Experiment:
    """
    Experiment class that allows to load and process and analyze DeepLabCut (DLC) output tabular files
    class arguments
    ----------
    path_experiment: str -> path to the folder containing the csv and video output from DLC organized as :

                    folder
                        L---->csvfiles: folder -> contains the csv files output from DLC
                        L---->videos: folder -> contains the videos files output from DLC

    likelihood_threshold: float -> threshold above which likelihood is considered as acceptable
    enable_iterative_imputer: bool -> data to be proceeded (or not) by sklearn.impute.IterativeImputer
    table_format: str -> extension of the tabular file
    video_format: str -> extension of the video file

    class attribute
    P.S.: I didn't put redundant arguments (i.e. self.path_experiment = path_experiment)
    ---------
    animal_list: list[object] -> list of Animal instances
    path_csv, path_video: str -> absolute path to the csv/video sub-folders
    list_csv, list_video: list[str] -> absolute path to all the csv/video to be treated
    config: dict -> dictionary of parameters of the experiment, contains in the txt file 'config.txt'
                - px_size: float -> size of a single pixel in videos (calibrated by the pixelCalib.py script)
                - zone_name: list[str] -> list of the zone name defined by the user

    class methods
    ---------
    load_animal: create an instance of the desired Animal class for every csv in list_csv
    analyze: analyze every animal contained in animal_list
    """
    deeplodocus_path = str(Path(__file__).parent)
    animal_list = []

    def __init__(
            self,
            path_experiment: str,
            likelihood_threshold: float = 0.9,
            enable_iterative_imputer: bool = True,
            table_format: str = '.csv',
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

        ######

        self.enable_iterative_imputer = enable_iterative_imputer

        Animal.likelihood_threshold = likelihood_threshold

        print('You have created an experiment')
        print("Use the '.load_animal' function to load datas\n")
    @property
    def config(self):
        config = Parser.load(self.deeplodocus_path + '/config.ini')
        # config['VIDEO']['fps_camera'] = cv2.VideoCapture(self.list_video[0]).get(cv2.CAP_PROP_FPS)
        # Parser.save(config, self.deeplodocus_path + '/config.ini')
        return config

    def load_animal(self, animal_model):
        """
        Create an instance of the desired Animal child-class for every csv in list_csv,
            and pre-process the data if desired
        Parameter:
        ----------
        animal_data: class -> desired Animal child-class
        """
        print("Loading the datas...")
        for csv in self.list_csv:
            animal_model(csv)

        for animal in self.animal_list:
            if self.enable_iterative_imputer:
                from DeepLodocus.newUtils import it_imputer
                animal.tracking_data = it_imputer(animal.tracking_data)

        print("Datas loaded")
        print("You can now use the '.analyze' function to process the data")

    def analyze(self,**behavior)

        print(self.config)
        for measurement in self.config['ANALYZE']:
            if measurement in behavior:
                self.config['ANALYZE'][measurement] = behavior[measurement]

        areas_dict = DictSerializer.loadJSON(self.deeplodocus_path + "/zone.txt")

        ## Create the empty dataframe_output ###
        columns = {"Animal ID": []}
        if self.config['ANALYZE']["distance"]:
            columns["Distance"] = []
        if self.config['ANALYZE']["time_zone"]:
            for zone in self.config['ZONE']["zone_name"]:
                columns[f"Time in {zone}"] = []

        if self.config['ANALYZE']["entries_zone"]:
            for zone in self.config['ZONE']["zone_name"]:
                columns[f"Entries in {zone}"] = []

        dataframe_output = pd.DataFrame(columns)
        ####

        for animal in self.animal_list:

            measurement = [animal.name]

            if self.config['ANALYZE']["distance"]:
                measurement.append(total_distance(animal.tracking_data[:, 6:8],
                                                  animal.likelihood[:, 3],
                                                  Animal.likelihood_threshold,
                                                  float(self.config['VIDEO']['fps_camera']),
                                                  float(self.config['VIDEO']['px_size'])
                                                  )
                                   )

            if self.config['ANALYZE']["time_zone"] or self.config['ANALYZE'][
                "entries_zone"]:  # TODO the total_time function is obsolete, needed to be update
                time_zone = total_time(
                    areas_dict,
                    animal.tracking_data,
                    animal.likelihood
                )
                print(time_zone)
                # if time_zone:
                #   measurement.append(time_zone)

                # if entries_zone:
                #   measurement.append(entries_zone)

            dataframe_output.loc[len(dataframe_output)] = measurement

        print('\n \nDatas __________________________________________________\n', dataframe_output)

        return dataframe_output


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
        self.cage = data_path.split('/')[-1][0]

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
        self.data_path = data_path
        Mouse.numMouse += 1
        Experiment.animal_list.append(self)
        print(f'Mouse {self.name} created')

    def __str__(self):
        return f"Mouse {self.name} in cage {self.cage}"

    def __repr__(self):
        return f"Mouse({self.data_path})"
