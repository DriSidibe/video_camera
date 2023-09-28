# Python program to save a
# video using OpenCV


import cv2
from datetime import datetime
import os, ffmpeg


def compress_video(video_full_path, output_file_name):
    # Reference: https://en.wikipedia.org/wiki/Bit_rate#Encoding_bit_rate
    min_audio_bitrate = 32000
    max_audio_bitrate = 256000

    probe = ffmpeg.probe(video_full_path)
    # Video duration, in s.
    duration = float(probe["format"]["duration"])
    # Best min size, in kB.
    best_min_size = (32000 + 100000) * (1.073741824 * duration) / (8 * 1024)
    # Audio bitrate, in bps.
    audio_bitrate = float(
        next((s for s in probe["streams"] if s["codec_type"] == "audio"), None)[
            "bit_rate"
        ]
    )
    # Target total bitrate, in bps.
    target_total_bitrate = (best_min_size * 1024 * 8) / (1.073741824 * duration)

    # Target audio bitrate, in bps
    if 10 * audio_bitrate > target_total_bitrate:
        audio_bitrate = target_total_bitrate / 10
        if audio_bitrate < min_audio_bitrate < target_total_bitrate:
            audio_bitrate = min_audio_bitrate
        elif audio_bitrate > max_audio_bitrate:
            audio_bitrate = max_audio_bitrate
    # Target video bitrate, in bps.
    video_bitrate = target_total_bitrate - audio_bitrate

    i = ffmpeg.input(video_full_path)
    ffmpeg.output(
        i, os.devnull, **{"c:v": "libx264", "b:v": video_bitrate, "pass": 1, "f": "mp4"}
    ).overwrite_output().run()
    ffmpeg.output(
        i,
        output_file_name,
        **{
            "c:v": "libx264",
            "b:v": video_bitrate,
            "pass": 2,
            "c:a": "aac",
            "b:a": audio_bitrate,
        },
    ).overwrite_output().run()


# Create an object to read
# from camera
video = cv2.VideoCapture(0)

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
result = cv2.VideoWriter(f"{filename}.avi", cv2.VideoWriter_fourcc(*"MJPG"), 10, size)

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

print("The video was successfully saved")
