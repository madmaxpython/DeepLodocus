"""
Created on Wed Apr 27 10:39:14 2022

@author: maximeteixeira
"""

import glob, os, sys
import pandas as pd
import numpy as np
from utils import TotalTime, TotalDistance, FileSaver
from shapely.geometry.polygon import Polygon
import json
from pathlib import Path
<<<<<<< Updated upstream

SCRIPT_PATH = str(Path(__file__).parent)

# Import config dictionary from a .txt file
with open(SCRIPT_PATH + '/config.txt', "r") as config_file:
    config = json.loads(config_file.read())


class Mouse():
    num_of_mice = 0
=======
from DeepLodocus.Utils import total_time, total_distance, DictSerializer, Parser
import cv2


class Experiment:
    """
    Experiment class allows to load, process and analyze DeepLabCut (DLC) output tabular files
    class arguments
    ----------
    path_experiment: str -> path to the folder containing the csv and video output from DLC organized as :
>>>>>>> Stashed changes

    def __init__(self, csvname):
        Mouse.num_of_mice += 1

        self.csvname = csvname
        self.cage = csvname[0]
        self.name = csvname.split('_')[1].split('.')[0]
        self.data = pd.read_csv(SCRIPT_PATH + '/Datas/' + self.csvname, header=[1, 2, 3], index_col=0)
        # Create an numpy array of likelihood value
        self.likelihood = np.array(self.data.loc[:, [x for x in self.data.columns.values if 'likelihood' in str(x)]])
        # Create a dataframe without likelihood columns
        columns_to_use = [x for x in self.data.columns.values if 'likelihood' not in str(x)]
        self.data_reduced = self.data.loc[:, columns_to_use]

<<<<<<< Updated upstream
    def analyze_zone(self):
=======
    class attribute
    P.S.: I didn't put redundant arguments (i.e. self.path_experiment = path_experiment)
    ---------
    animal_list: list[object] -> list of Animal instences
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
            print(f"Different number of tabular files (n={len(self.list_csv)}) and videos (n={len(self.list_video)}")

        ######

        self.enable_iterative_imputer = enable_iterative_imputer

        Animal.likelihood_threshold = likelihood_threshold

        print('You have created an experiment')
        print("Use the '.load_animal' function to load datas\n")
    @property
    def config(self):
        config = Parser.load(self.deeplodocus_path + '/config.ini')
        #config['VIDEO']['fps_camera'] = cv2.VideoCapture(self.list_video[0]).get(cv2.CAP_PROP_FPS)
        #Parser.save(config, self.deeplodocus_path + '/config.ini')
        return config

    def load_animal(self, animal_model):
>>>>>>> Stashed changes
        """
            #Create a Shapely Polygon-object for each zone define by the user
            Polygon object have has the attribute ".contain" to check if a point is in this Polygon
            We will use this attribute to see if mice is in zone

            #Call the function analysis.TotalTime, that measure time and nb of entries in zone for each zone
            Output -> dictionary 'output_zone' with 'time_zone' and 'entries_zone' as key, saved in self.time_zone and
            self.entries_zone respectively
        """
        with open(SCRIPT_PATH + "/zone.txt", "r") as zone_file:
            areas = json.loads(zone_file.read())

        for zone in areas:
            areas[zone] = Polygon(areas[zone])

        output_zone = TotalTime(config, areas, self.data_reduced, self.likelihood, self.cage)
        self.time_zone = output_zone['time_zone']
        self.entries_zone = output_zone['entries_zone']

<<<<<<< Updated upstream
    def analyze_distance(self):
        """
            Measure the total distance travelled by the mice during the session
            Output -> the distance travelled, save in self.distance_travelled
        """
        self.distance_travelled = TotalDistance(config, self.data_reduced, self.likelihood)
=======
    def analyze(self,**behavior
                ):
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

            if self.config['ANALYZE']["time_zone"] or self.config['ANALYZE']["entries_zone"]:  # TODO the total_time function is obsolete, needed to be update
                time_zone  = total_time(
                                                     areas_dict,
                                                     animal.tracking_data,
                                                     animal.likelihood
                                                     )
                print(time_zone)
                #if time_zone:
                 #   measurement.append(time_zone)

                #if entries_zone:
                 #   measurement.append(entries_zone)

            dataframe_output.loc[len(dataframe_output)] = measurement

        print('\n \nDatas __________________________________________________\n', dataframe_output)

        return dataframe_output
>>>>>>> Stashed changes


if __name__ == "__main__":
    # Create an empty dataframe that will be filed by analyze for each mouse (distance travelled, time & entries in zone)
    df_analysis = pd.DataFrame()

<<<<<<< Updated upstream
    # Look for csv files, and create an instance Mouse for each of them
    for file in glob.glob(os.path.join(SCRIPT_PATH, 'Datas', "*.csv")):
        mouse_id = glob.glob(os.path.join(SCRIPT_PATH, 'Datas', "*.csv")).index(file)
        globals()[f"mouse_{mouse_id}"] = Mouse(file.split("Datas/", 1)[1])
        df_analysis[globals()[f"mouse_{mouse_id}"].name] = 0
=======
    def __init__(self, data_path):
        self.name = data_path.split('_')[1].split('.')[0]
        self.cage = data_path.split('/')[-1][0]

        self.data = pd.read_csv(data_path, header=[2, 3], index_col=0)

        self.likelihood = np.array(self.data.loc[:, [x for x in self.data.columns.values if
                                                     'likelihood' in str(x)]],
                                   dtype='float16') > self.likelihood_threshold


        self.tracking_data = np.array(self.data.loc[:, [x for x in self.data.columns.values if not
        'likelihood' in str(x)]], dtype='float32')
>>>>>>> Stashed changes


########The following list will be used to fill df_analyze dataframe

    # If time or entries in zones need to be analyze, create a list for each of them
    if config['analyse_zone'] == True or config['analyse_entries'] == True:
        for zone in config['zone_name']:
            globals()[f"list_time_{zone}"] = []
            globals()[f"list_entries_{zone}"] = []

    # If distance travelled need to be analyzed, create a list
    if config['analyse_distance']:
        list_distance = []

    # For each measure, fill the list create above with measure
    for mice_nb in range(Mouse.num_of_mice):
        if config['analyse_zone'] or config['analyse_entries']:

            globals()[f"mouse_{mice_nb}"].analyze_zone()

            for zone in config['zone_name']:

                if config['analyse_zone']:
                    globals()[f"list_time_{zone}"].append(globals()[f"mouse_{mice_nb}"].time_zone[zone])

                if config['analyse_entries']:
                    globals()[f"list_entries_{zone}"].append(globals()[f"mouse_{mice_nb}"].entries_zone[zone])

                # If it is the last mouse, create a row in dataframe made of the list of this measure
                if mice_nb == Mouse.num_of_mice - 1:
                    if config['analyse_zone']:
                        df_analysis.loc['Time in zone ' + zone + ' (sec)'] = globals()[f"list_time_{zone}"]

                    if config['analyse_entries']:
                        df_analysis.loc['Entries in ' + zone] = globals()[f"list_entries_{zone}"]

        if config['analyse_distance']:
            globals()[f"mouse_{mice_nb}"].analyze_distance()
            list_distance.append(globals()[f"mouse_{mice_nb}"].distance_travelled)
            # If it is the last mouse, create a row in dataframe made of the list of this measure
            if mice_nb == Mouse.num_of_mice - 1:
                df_analysis.loc['Distance travelled (cm)'] = list_distance

    FILE_PATH = str(sys.argv[1])
    print('\n \nData CPP Video __________________________________________________\n', df_analysis)
    df_analysis.to_excel(FILE_PATH
                         )
