import glob
import os
import pandas as pd
import numpy as np
from pathlib import Path
from DeepLodocus.newUtils import total_time, total_distance, DictSerializer

SCRIPT_PATH = str(Path(__file__).parent)


class Config:
    def __init__(self, configfile):
        for key in configfile:  # set attribute for every keys of the dictionary
            setattr(self, key, configfile[key])


class Animal:
    """
    Create an animal from a tabular file using info in the name.
    (Created if we want to add new animal models to DeepLodocus)
    Args:
        datapath (str): path of the tabular file
    self:
        name (str) : experimental name of the animal
        cage (str) : cage associate with a camera where Animal behaved
        data (pd.Dataframe) : DeepLabCut output tracking data
    """
    animal_list = []

    def __init__(self, data_path, threshold):
        self.name = data_path.split('_')[1].split('.')[0]
        self.cage = data_path[0]
        self.data = pd.read_csv(data_path, header=[2, 3], index_col=0)
        self.threshold = threshold

    @property
    def likelihood(self):
        """
        Extract likelihood columns from self.data in np.arrays
        Args:
            self.data (pd.Dataframe): DeepLabCut output tracking data
        Returns:
            likelihood(np.arrays)
        """
        return np.array(self.data.loc[:, [x for x in self.data.columns.values if 'likelihood' in str(x)]],
                        dtype='float16') > self.threshold

    @property
    def datatracking(self):
        """
        Extract tracking datas columns from self.data in np.arrays
        Args:
            self.data (pd.Dataframe): DeepLabCut output tracking data
        Returns:
            datatracking(np.arrays)
        """
        return np.array(self.data.loc[:, [x for x in self.data.columns.values if not 'likelihood' in str(x)]],
                        dtype='float32')


class Mouse(Animal):
    """
    Child of Animal class for Mouse
    """
    numMouse = 0

    def __init__(self, data_path, threshold=0.9):
        super().__init__(data_path, threshold)
        Mouse.numMouse += 1
        Animal.animal_list.append(self)
        self.body_part = 9


class AnimalAnalyzer:
    def __init__(self, name, tracking_data, likelihood):
        self.name = name
        self.tracking_data = tracking_data
        self.likelihood = likelihood
        print(self.name)

    @property
    def DataFrame_Results(self):
        dictio = {'name': []}
        if CONFIG.analyse_distance:
            dictio['Distance'] = []
        if CONFIG.analyze_zone:
            for zone in CONFIG['zone_name']:
                dictio['Time_' + zone] = []
        if CONFIG.analyze_entries:
            for zone in CONFIG['zone_name']:
                dictio['Entries_' + zone] = []
        return pd.DataFrame(dictio)

    def analyse(self):
        measurement = [self.name]
        if CONFIG.analyse_distance:
            distance_travelled = total_distance(self.tracking_data[:, 6:8], self.likelihood[:, 3], CONFIG.fps_camera,
                                                CONFIG.px_size)
            measurement.append(distance_travelled)

        if CONFIG.analyse_zone or CONFIG.analyse_entries:
            time_zone, entries_zone = total_time(CONFIG, AREAS, self.tracking_data, self.likelihood, self.cage)
            if CONFIG.analyse_zone:
                measurement.append(time_zone)
            if CONFIG.analyse_entries:
                measurement.append(entries_zone)
        AnimalAnalyzer.df_Results.loc[len(AnimalAnalyzer.df_Results)] = measurement


def data_to_csv(dataframe: pd.DataFrame, FILE_PATH):
    print('\n \nData __________________________________________________\n', dataframe)
    return dataframe.to_csv(FILE_PATH)


CONFIG = Config(DictSerializer.loadJSON(SCRIPT_PATH + '/config.txt'))
AREAS = DictSerializer.loadJSON(SCRIPT_PATH + "/zone.txt")
listCSV = glob.glob(os.path.join(SCRIPT_PATH, 'Datas', "*.csv"))
