# Python program to save a
# video using OpenCV


import cv2
from datetime import datetime

cap = cv2.VideoCapture(0)


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


video_res = (160, 100)


try:
    # Create an object to read
    # from camera
    video = cv2.VideoCapture(0)

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
        f"{filename}.avi", cv2.VideoWriter_fourcc(*"MJPG"), 5, size
    )

    while True:
        ret, frame = video.read()

        if ret == True:
            # Write the frame into the
            # file 'filename.avi'
            result.write(frame)

            # Display the frame
            # saved in the file
            cv2.imshow("Frame", frame)

            # Press S on keyboard
            # to stop the process
            if cv2.waitKey(1) & 0xFF == ord("s") or datetime.now().hour == 19:
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

    # Compress input.avi to 50MB and save as output.avi
    # compress_video(f"C:\\Users\\dsidi.DARKER\\{filename}.avi", f"{filename}.avi")

    print(f"The video {filename} was successfully saved")
except:
    # Create an object to read
    # from camera
    video = cv2.VideoCapture(0)

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
        f"{filename}.avi", cv2.VideoWriter_fourcc(*"MJPG"), 5, size
    )

    while True:
        ret, frame = video.read()

        if ret == True:
            # Write the frame into the
            # file 'filename.avi'
            result.write(frame)

            # Display the frame
            # saved in the file
            cv2.imshow("Frame", frame)

            # Press S on keyboard
            # to stop the process
            if cv2.waitKey(1) & 0xFF == ord("s") or datetime.now().hour == 19:
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

    # Compress input.avi to 50MB and save as output.avi
    # compress_video(f"C:\\Users\\dsidi.DARKER\\{filename}.avi", f"{filename}.avi")

    print(f"The video {filename} was successfully saved")
