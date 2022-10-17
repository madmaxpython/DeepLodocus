import pandas as pd
import numpy as np
from pathlib import Path
from DeepLodocus.newUtils import total_time, total_distance, DictSerializer

SCRIPT_PATH = str(Path(__file__).parent)


class Config:
    def __init__(self, configfile):
        self.px_size = configfile['px_size']
        self.fps_camera = configfile['fps_camera']
        self.analyze_distance = configfile['analyze_distance']
        self.analyze_zone = configfile['analyze_zone']
        self.analyze_entries = configfile['analyze_entries']
        self.zone_name = configfile['zone_name']


CONFIG = Config(DictSerializer.loadJSON(SCRIPT_PATH + '/config.txt'))


def DataFrame_factory():
    dictio = {'Animal ID': []}
    if CONFIG.analyze_distance:
        dictio['Distance'] = []
    if CONFIG.analyze_zone:
        for zone in CONFIG.zone_name:
            dictio['Time_' + zone] = []
    if CONFIG.analyze_entries:
        for zone in CONFIG.zone_name:
            dictio['Entries_' + zone] = []
    return pd.DataFrame(dictio)


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
    animal_list = []
    DataFrame_Results = DataFrame_factory()

    def __init__(self, data_path, threshold):
        self.name = data_path.split('_')[1].split('.')[0]
        self.cage = data_path[0]
        self.data = pd.read_csv(data_path, header=[2, 3], index_col=0)
        self.threshold = threshold

    @property
    def likelihood(self) -> np.array:
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
    def tracking_data(self) -> np.array:
        """
        Extract tracking datas columns from self.data in np.arrays
        Args:
            self.data (pd.Dataframe): DeepLabCut output tracking data
        Returns:
            datatracking(np.arrays)
        """
        return np.array(self.data.loc[:, [x for x in self.data.columns.values if not 'likelihood' in str(x)]],
                        dtype='float32')

    def analyse(self):
        measurement = [self.name]
        if CONFIG.analyze_distance:
            distance_travelled = total_distance(self.tracking_data[:, 6:8], self.likelihood[:, 3], CONFIG.fps_camera,
                                                CONFIG.px_size)
            measurement.append(distance_travelled)

        if CONFIG.analyze_zone or CONFIG.analyze_entries:
            time_zone, entries_zone = total_time(CONFIG, AREAS, self.tracking_data, self.likelihood, self.cage)
            if CONFIG.analyze_zone:
                measurement.append(time_zone)
            if CONFIG.analyze_entries:
                measurement.append(entries_zone)

        Animal.DataFrame_Results.loc[len(Animal.DataFrame_Results)] = measurement


class Mouse(Animal):
    """
    Child of Animal class for Mouse
    """
    numMouse = 0
    body_part = 9
    head = ['nose', 'leftear', 'rightear']
    body = ['spine1', 'spine2', 'spine3']
    tail = ['tailbase', 'tailmid', 'tailend']
    body_parts = head + body + tail
    body_sections = {'head': head, 'body': body, 'tail': tail}

    def __init__(self, data_path, threshold=0.9):
        super().__init__(data_path, threshold)
        Mouse.numMouse += 1
        Animal.animal_list.append(self)


def load_mice(list_csv: list, threshold: int = 0.9):
    for csv in list_csv:
        Mouse(csv, threshold)


def data_to_csv(dataframe: pd.DataFrame, FILE_PATH):
    print('\n \nData __________________________________________________\n', dataframe)
    return dataframe.to_csv(FILE_PATH)


AREAS = DictSerializer.loadJSON(SCRIPT_PATH + "/zone.txt")

