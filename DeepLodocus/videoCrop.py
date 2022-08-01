import cv2
import datetime
import time
from tkinter import Tk, Entry, Button, Label, filedialog


def OutputName():
    """
    This function pop a window in which user will give a output name of the cropped video
    :return:FileName -> Name of the output video
    """

    def saveFct():
        FileName = str(e1.get())
        if FileName != "":
            master.quit()
            return FileName

    master = Tk()
    Label(master, text="Output File Name").grid(row=0)
    master.title("Save Your File")

    e1 = Entry(master)
    e1.grid(row=0, column=1)

    b1 = Button(master,
                text='Save',
                command=saveFct)

    b1.grid(row=0, column=2)

    master.mainloop()

    return saveFct()


class videocropper():
    """
    Class of the video to be cropped.
    Using openCV, will determine few parameters (video length, format, FPS).
    User will use 2 slider to determine the beginning and end of the desired cropped video

    """

    def __init__(self, videopath):

        def getFrame(frame_nr):
            """
            Will display the video at the timeframe selected by the slider
            :param frame_nr: timeframe
            """
            self.video.set(cv2.CAP_PROP_POS_FRAMES, frame_nr)

        self.video = cv2.VideoCapture(videopath)

        self.video_length = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.video_width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.video_height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.FPS = int(self.video.get(cv2.CAP_PROP_FPS))

        cv2.namedWindow("Video")

        cv2.setWindowTitle("Video", videopath)

        cv2.createTrackbar("Start", "Video", 0, self.video_length, getFrame)

        cv2.createTrackbar("End", "Video", 0, self.video_length, getFrame)

        while 1:
            START_VIDEO = cv2.getTrackbarPos("Start", 'Video')
            END_VIDEO = cv2.getTrackbarPos("End", 'Video')

            ret, frame = self.video.read()

            if ret:
                cv2.imshow("Video", frame)

            else:
                pass

            key = cv2.waitKey(self.FPS)

            if key == ord('q'):
                outputname = OutputName()
                start_time = time.time()

                print("Start at {} (frame {})".format(str(datetime.timedelta(seconds=START_VIDEO/self.FPS)), START_VIDEO))
                print("End at {} (frame {})".format(str(datetime.timedelta(seconds=END_VIDEO/self.FPS)), END_VIDEO))

                fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                writer = cv2.VideoWriter('{}.mp4'.format(outputname), fourcc, self.FPS,
                                         (self.video_width, self.video_height))

                for i in range(START_VIDEO, END_VIDEO):
                    ret, frame = self.video.read()
                    if ret:
                        if START_VIDEO < i:
                            writer.write(frame)

                writer.release()
                self.video.release()
                cv2.destroyAllWindows()
                print("Cropping excution lasted %s seconds" % (time.time() - start_time))
                # release resources
                break


if __name__ == "__main__":
    """
    1. Open a finder window to select video to be cropped
    2. Crop video selected video by creating an instance of the 'videocropper' class for each of them
    """
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilenames()

    for file in file_path:
        videocropper(file)
