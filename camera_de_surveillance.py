# Python program to save a
# video using OpenCV


import cv2
from datetime import datetime
import os
import subprocess
import time

start_time = 7
end_time = 19
launch_now = True
video_dir = "/home/drissa/Bureau/video_surveillance/"
tmp_dir = "/tmp/"
video_ext = ".avi"


def make_1080p(camera):
    camera.set(3, 1920)
    camera.set(4, 1080)


def make_720p(camera):
    camera.set(3, 1280)
    camera.set(4, 720)


def make_480p(camera):
    camera.set(3, 640)
    camera.set(4, 480)


def change_res(camera, width, height):
    camera.set(3, width)
    camera.set(4, height)

def resize_image(src, scale=0.5):
    return cv2.resize(src, (int(src.shape[0]*scale), int(src.shape[1]*scale)))


video_res = (160, 100)


def capture():
    global launch_now
    try:
        # Create an object to read
        # from camera
        video = cv2.VideoCapture(2)
        start_timestamp = datetime.now().timestamp()
        pass_hour = 0
        pass_minute = 0
        pass_second = 0

        change_res(video, *video_res)
        # change_res(1280, 720)

        # We need to check if camera
        # is opened previously or not
        if video.isOpened() == False:
            print("Error reading video file")

        # We need to set resolutions.
        # so, convert them from float to integer.
        frame_width = int(video.get(3))
        frame_height = int(video.get(4))

        size = (frame_width, frame_height)

        # Below VideoWriter object will create
        # a frame of above defined The output
        # is stored in 'filename.avi' file.
        filename = "_".join(
            "_".join(
                "_".join("_".join(str(datetime.now()).split(" ")).split(":")).split("-")
            ).split(".")
        )
        result = cv2.VideoWriter(
            f"{tmp_dir}{filename}.avi", cv2.VideoWriter_fourcc(*"MJPG"), 15, size
        )

        while True:
            ret, frame = video.read()

            if ret == True:
                #display video current time
                tmp2 = datetime.now().timestamp()
                tmp = int(tmp2 - start_timestamp)
                if tmp == 1:
                    pass_second = pass_second + 1
                    tmp = 0
                    start_timestamp = tmp2

                if pass_second == 60:
                    pass_minute = pass_minute + 1
                    pass_second = 0

                if pass_minute == 60:
                    pass_hour = pass_hour + 1
                    pass_minute = 0

                complet_pass_time = f"{pass_hour} : {pass_minute} : {pass_second}"

                #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.putText(frame ,str(datetime.now()), (0, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0), 1, cv2.LINE_4)

                #frame = resize_image(frame)

                # Write the frame into the
                # file 'filename.avi'
                result.write(frame)

                # Display the frame
                # saved in the file
                cv2.imshow("Frame", frame)

                # Press S on keyboard
                # to stop the process
                if datetime.now().hour == end_time or cv2.waitKey(1) & 0xFF == ord("s"):
                    break


            # Break the loop
            else:
                break

        # When everything done, release
        # the video capture and video
        # write objects
        video.release()
        result.release()

        # Closes all the frames
        cv2.destroyAllWindows()

        time.sleep(3)
        print("compressing the video ...")
        subprocess.run(["ffmpeg", "-i", tmp_dir+filename+video_ext, "-s", "160x120", "-vcodec", "msmpeg4v2", video_dir+filename+video_ext])
        subprocess.run(["rm", tmp_dir+filename+".avi"])

        print(f"The video {filename} was successfully saved")
    except:
        exit()


while True:
    if datetime.now().weekday() != 6:
        capture()

    if datetime.now().hour == end_time:
        time.sleep(43200)
