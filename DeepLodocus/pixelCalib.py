import matplotlib.pyplot as plt
import random
from numpy import sqrt as sqrt
from tkinter import Tk, simpledialog
from matplotlib.widgets import PolygonSelector
from Utils import DictSerializer, file_selector, AskInput
import cv2
import yaml
from matplotlib.widgets import Button


class LineBuilder:
    def __init__(self, line):
        self.line = line
        self.xs = list(line.get_xdata())
        self.ys = list(line.get_ydata())
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self.draw)
        self.keypress = line.figure.canvas.mpl_connect('key_press_event', self.key)

    def draw(self, event):
        if len(self.xs) < 2:
            self.xs.append(event.xdata)
            self.ys.append(event.ydata)

            self.line.set_data(self.xs, self.ys)
            self.line.figure.canvas.draw()
    def key(self, event):
        if event.key == 'q':
            plt.close('all')

        if event.key == 'a':
            self.line.set_data([], [])
            self.ys, self.xs = [], []
            self.line.figure.canvas.draw()



def ploter(filepath):
    fig, ax = plt.subplots()
    ax.invert_yaxis()
    fig.canvas.manager.set_window_title('Calibration Step')

    video = cv2.VideoCapture(filepath)
    randomnb = random.randint(0, int(video.get(cv2.CAP_PROP_FRAME_COUNT)))
    video.set(1, randomnb)
    fig.suptitle('Calibration', fontsize=16)

    ret, frame = video.read()
    imgplot = plt.imshow(frame)

    line, = ax.plot([], [])
    linebuilder = LineBuilder(line)

    plt.show()
    return(linebuilder.line.get_data())


def Calibrator (video_path, CONFIG_PATH):

    coord = ploter(video_path)

    distance_px = sqrt((coord[0][0] - coord[1][0]) ** 2 + (coord[0][1] - coord[1][1]) ** 2)

    distance_cm = AskInput('Calibration', 'Size in cm (use "." as decimal separator)', float).get_entry()

    pixel_size = distance_cm / distance_px

    return pixel_size



Calibrator('/Users/maximeteixeira/Desktop/DeepLodocusGit/DeepLodocus/Datas/videos/1_10BR.mp4', '/Users/maximeteixeira/Desktop/DeepLodocusGit/DeepLodocus/Datas/config.yaml')