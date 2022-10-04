import matplotlib.pyplot as plt
import random
from numpy import sqrt as sqrt
from tkinter import Tk, simpledialog
from newUtils import dictSerializer, FileSelector
import cv2


class Calibrator:
    def __init__(self, TITLE_WINDOW, VIDEO_PATH):
        self.TITLE_WINDOW = TITLE_WINDOW
        self.VIDEO_PATH = VIDEO_PATH
        self.point = []

    def selector(self):
        self.fig, ax = plt.subplots()
        ax.invert_yaxis()
        self.fig.canvas.manager.set_window_title('Calibration Step')
        self.fig.suptitle(self.TITLE_WINDOW, fontsize=16)

        cap = cv2.VideoCapture(self.VIDEO_PATH)
        randomnb = random.randint(0, 300)
        cap.set(1, randomnb)

        ret, frame = cap.read()
        imgplot = plt.imshow(frame)
        self.fig.canvas.mpl_connect('button_press_event', self.onClick)
        plt.show()
        plt.close('all')
        return self.point

    def onClick(self, event):
        self.point.append((event.xdata, event.ydata))
        if len(self.point) == 2:
            plt.close('all')



def tkAskFloat(WINDOW_TITLE, GRID_TITLE):
    root = Tk()
    file_path = simpledialog.askfloat(title=WINDOW_TITLE, prompt=GRID_TITLE)
    root.mainloop()
    return file_path

filepath = FileSelector('Select video to calibrate', False, [("Video files", ".mp4 .MOV .avi")])

calib = Calibrator("Calib", filepath)

coord = calib.selector()

distance_px = sqrt((coord[0][0] - coord[1][0]) ** 2 + (coord[0][1] - coord[1][1]) ** 2)

distance_cm = float(input('Size in cm: '))

pixel_size = float(distance_cm/distance_px)

config = dictSerializer.loadJSON("config.txt")

config["px_size"]=pixel_size

dictSerializer.saveJSON(config, "config.txt")
