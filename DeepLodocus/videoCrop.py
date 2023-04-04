import cv2
import datetime
import time
from Utils import AreaSelector, file_selector, file_saver


class videocropper:
    """
    Class of the video to be cropped.
    Using openCV, will determine few parameters (video length, format, FPS).
    User will use 2 slider to determine the beginning and end of the desired cropped video
    """

    def __init__(self, videopath):


        self.video = cv2.VideoCapture(videopath)
        self.video_extension = videopath.split(".")[-1]
        self.video_length = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.video_width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.video_height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.FPS = int(self.video.get(cv2.CAP_PROP_FPS))
        self.cropped = False

        def getFrame(frame_nr):
            """
            Will display the video at the timeframe selected by the slider
            :param frame_nr: timeframe
            """
            self.video.set(cv2.CAP_PROP_POS_FRAMES, frame_nr)

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
            if key == ord('c'):

                coord = AreaSelector(videopath).polygon_selector("Crop your video")
                x_list, y_list = [x_tuple[0] for x_tuple in coord], [y_tuple[1] for y_tuple in coord]
                x_min, x_max, y_min, y_max = int(min(x_list)), int(max(x_list)), int(min(y_list)), int(max(y_list))

                self.video_width = int(x_max - x_min)
                self.video_height = int(y_max - y_min)
                self.cropped = True

            if key == ord('q'):

                print(f"Start at {str(datetime.timedelta(seconds=START_VIDEO / self.FPS))}")
                print(f"End at {str(datetime.timedelta(seconds=END_VIDEO / self.FPS))}")
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')

                writer = cv2.VideoWriter(f'test.mp4', fourcc, self.FPS,
                    (self.video_width, self.video_height))

                start_time = time.time()
                print(START_VIDEO, END_VIDEO)
                for i in range(START_VIDEO, END_VIDEO):
                    ret, frame = self.video.read()
                    if ret:
                        if START_VIDEO < i and self.cropped:
                            crop_frame = frame[y_min:y_max, x_min:x_max]
                            writer.write(crop_frame)
                        elif START_VIDEO < i and not self.cropped:
                            writer.write(frame)

                writer.release()
                self.video.release()

                cv2.destroyAllWindows()
                print(f"Cropping execution lasted {(time.time() - start_time)} seconds")
                break


if __name__ == "__main__":
    """
    1. Open a finder window to select video to be cropped
    2. Crop video selected video by creating an instance of the 'videocropper' class for each of them
    """
    file_path = file_selector("Select video(s) to edit", True, [("Video files", ".mp4 .MOV .avi")])

    for file in file_path:
        videocropper(file)
