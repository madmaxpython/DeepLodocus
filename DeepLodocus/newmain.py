import glob
import os, sys
import pandas as pd
import numpy as np
from pathlib import Path
from DeepLodocus.utils import TotalDistance, TotalTime, dictSerializer

SCRIPT_PATH = str(Path(__file__).parent)


class Config:
    def __init__(self, configfile):
        self.fps_camera = configfile["fps_camera"]
        self.px_size = configfile["px_size"]
        self.path_env = configfile["path_env"]
        self.output_excel = configfile["output_excel"]
        self.nb_cage = configfile["nb_cage"]
        self.zone_name = configfile["zone_name"]
        self.analyse_distance = configfile["analyse_distance"]
        self.analyse_zone = configfile["analyse_zone"]
        self.analyse_entries = configfile["analyse_entrie"]


class Animal:
    """
    Create an animal from a tabular file using info in the name.
    Created if we want to add new animal models to DeepLodocus
    Args:
        datapath (str): path of the tabular file
    self:
        name (str) : experimental name of the animal
        cage (str) : cage associate with a camera where Animal behaved
        data (pd.Dataframe) : DeepLabCut output tracking data
    """

    def __init__(self, datapath):
        self.name = datapath.split('_')[1].split('.')[0]
        self.cage = datapath[0]
        self.data = pd.read_csv(datapath, header=[1, 2, 3], index_col=0)

    @property
    def likelihood(self):
        """
        Extract likelihood columns from self.data in np.arrays
        Args:
            self.data (pd.Dataframe): DeepLabCut output tracking data

        Returns:
            likelihood(np.arrays)
        """
        return np.array(self.data.loc[:, [x for x in self.data.columns.values if 'likelihood' in str(x)]])

    @property
    def datatracking(self):
        """
        Extract tracking datas columns from self.data in np.arrays
        Args:
            self.data (pd.Dataframe): DeepLabCut output tracking data

        Returns:
            datatracking(np.arrays)
        """
        columns_to_use = [x for x in self.data.columns.values if 'likelihood' not in str(x)]
        return self.data.loc[:, columns_to_use]


class Mouse(Animal):
    """
    Child of Animal class for Mouse
    """
    numMouse = 0
    listMouse = []

    def __init__(self, name, cage, data):
        super.__init__(name, cage, data)
        Mouse.numMouse += 1
        self.bodypart = 9


class animalAnalyzer:  # TODO check how to manage heritance
    df_Results = pd.DataFrame()  # TODO ajouter les bonnes colonnes

    def __init__(self, animalToAnalyze):
        self.trackingData = animalToAnalyze.trackingData
        self.likelihood = animalToAnalyze.likelihood
        self.cage = animalToAnalyze.cage
        self.name = animalToAnalyze.name

    def analyse(self):
        measurement = [self.name]
        if CONFIG.analyse_distance:
            distance_travelled = TotalDistance(CONFIG, self.trackingData, self.likelihood)
            measurement.append(distance_travelled)

        if CONFIG.analyse_zone or CONFIG.analyse_entries:
            time_zone, entries_zone = TotalTime(CONFIG, AREAS, self.trackingData, self.likelihood, self.cage)
            if CONFIG.analyse_zone:
                measurement.append(time_zone)
            if CONFIG.analyse_entries:
                measurement.append(entries_zone)

        animalAnalyzer.df_Results.loc[len(animalAnalyzer.df_Results.loc)] = measurement


if __name__ == "__main__":
    CONFIG = Config(dictSerializer.loadJSON(SCRIPT_PATH + '/config.txt'))
    AREAS = dictSerializer.loadJSON(SCRIPT_PATH + "/zone.txt")
    listCSV = glob.glob(os.path.join(SCRIPT_PATH, 'Datas', "*.csv"))

    for csv in listCSV:
        mouse_id = f"mouse_{listCSV.index(csv)}"
        globals()[mouse_id] = Mouse(csv.split("Datas/", 1)[1])

    FILE_PATH = str(sys.argv[1])
    print('\n \nData CPP Video __________________________________________________\n', animalAnalyzer.df_Results)

    animalAnalyzer.df_Results.to_excel(FILE_PATH)
