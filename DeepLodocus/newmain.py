import glob
import os, sys
import pandas as pd
import numpy as np
from pathlib import Path
from DeepLodocus.utils import TotalDistance, TotalTime, dictSerializer

SCRIPT_PATH = str(Path(__file__).parent)


class Config:
    def __init__(self, configfile):
        for key in configfile: #set attribute for every keys of the dictionary
            setattr(self, key, configfile[key])


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
        self.data = pd.read_csv(datapath, header=[2, 3], index_col=0)  # TODO import maybe just the header

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
        return np.array(self.data.loc[:, [x for x in self.data.columns.values if not 'likelihood' in str(x)]])


class Mouse(Animal):
    """
    Child of Animal class for Mouse
    """
    numMouse = 0
    listMouse = []

    def __init__(self, datapath):
        super().__init__(datapath)
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
        measurement = [self.name] #List with animal name will be filled with measurement and add to the final output dataframe
        if CONFIG.analyse_distance:
            distance_travelled = TotalDistance(self.trackingData[:, 6:8], self.likelihood[:, 3], CONFIG.fps_camera,
                                               CONFIG.px_size)
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
        animal_id = f"animal_{listCSV.index(csv)}"
        globals()[animal_id] = Mouse(csv.split("Datas/", 1)[1])

    FILE_PATH = str(sys.argv[1])
    print('\n \nData CPP Video __________________________________________________\n', animalAnalyzer.df_Results)

    animalAnalyzer.df_Results.to_excel(FILE_PATH)
