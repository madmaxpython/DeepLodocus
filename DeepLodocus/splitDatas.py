import pandas as pd
from matplotlib.widgets import TextBox
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import cv2
from Utils import file_selector

SCRIPT_PATH = str(Path(__file__).parent)


class Mouse:
    NB_MICE = 0
    NB_BP = 9
    message = "Provide the mouse ID"

    def __init__(self, data: pd.DataFrame, videopath):
        self.data = data
        self.video = videopath
        self.data_tracking = np.array(
            self.data.loc[3:, [x for x in self.data.columns.values if not 'likelihood' in str(x)]])
        self.name = AnimalSelector(self.video).video_plot(self.message, self.data_tracking[60])
        self.data.to_csv(f'Datas/{self.name}.csvfiles')


class Mouse_Manager:
    def __init__(self, datapath, videocalib):
        self.data = pd.read_csv(datapath, index_col=0, header=[2, 3])
        self.video = videocalib
        Mouse.NB_MICE = int(len(self.data.columns) / (Mouse.NB_BP * 3))
        for x in range(Mouse.NB_MICE):
            globals()[f"mouse{x + 1}"] = Mouse(self.data.iloc[:, x * 27:(1 + x) * 27], self.video)


class AnimalSelector:
    def __init__(self, VIDEO_PATH: str):
        self.VIDEO_PATH = VIDEO_PATH
        self.lineprops = {'color': 'red', 'linewidth': 4, 'alpha': 0.8}
        self.point = []

    @staticmethod
    def submit(text):
        plt.close("all")
        return text

    def video_plot(self, TITLE_WINDOW, data_tracking) -> str:
        self.fig, self.ax = plt.subplots()
        self.ax.invert_yaxis()
        self.fig.canvas.manager.set_window_title('Calibration Step')
        self.video = cv2.VideoCapture(self.VIDEO_PATH)
        self.video_lenght = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))

        for x in range(0, 17, 2):
            plt.plot(data_tracking[x], data_tracking[x + 1], 'ro')

        self.video.set(1, 1)
        self.fig.suptitle(TITLE_WINDOW, fontsize=16)

        ret, frame = self.video.read()
        image_plot = plt.imshow(frame)
        axbox = plt.axes([0.1, 0.05, 0.8, 0.075])
        text_box = TextBox(axbox, 'Name:')
        text_box.on_submit(self.submit)
        plt.show()
        return text_box.text


if __name__ == '__main__':
    CSV_TO_TREAT = file_selector('Select data to split', True, [("Tabular file", "*.csvfiles")])
    print(CSV_TO_TREAT)

    for file in CSV_TO_TREAT:
        print("csvfiles file to split: ", file)

        CALIBRATION_VIDEO = file_selector(f"Select video for {file.split('/')[-1]}", False, [("Video files", ".mp4 .MOV .avi")])[0]
        Mouse_Manager(file, CALIBRATION_VIDEO)