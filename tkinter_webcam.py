import tkinter as tk
import cv2
from PIL import Image, ImageTk
import threading

class VideoCamera:
    isRecording = False
    frame = None
    frameImage = None
    capture_object = None
    close = False

    def __init__(self):
        self.win_width, self.win_height = 800, 600
        self.video_width, self.video_height = 320, 240

        # main window
        self.root = tk.Tk()

        # components
        self.left_cnt = tk.Frame(self.root, bg="red", width=int(self.win_width/3), highlightbackground="black", highlightthickness=1)
        self.right_cnt = tk.Frame(self.root, bg="blue", highlightbackground="black", highlightthickness=1)
        self.video_ctn = tk.Frame(self.right_cnt, bg="yellow", width=int(self.video_width+self.video_width/2), height=int(self.video_height+self.video_height/2), highlightbackground="black", highlightthickness=1)
        self.video = tk.Label(self.video_ctn)
        self.start_recording_btn = tk.Button(self.video_ctn, text="start recording",command=self.run_camera)
        self.stop_recording_btn = tk.Button(self.video_ctn, text="stop recording",command=self.stop_camera)

        #settings
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)
        self.root.geometry(f"{self.win_width}x{self.win_height}")
        self.root.resizable(False, False)
        self.root.title("pycamy")
        self.stop_recording_btn.configure(state="disabled")

        # components packing
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=2)
        self.root.rowconfigure(0, weight=1)
        self.left_cnt.grid(row=0, column=0, sticky="nswe")
        self.right_cnt.grid(row=0,column=1, sticky="ns")
        self.right_cnt.columnconfigure(0, weight=1)
        self.video_ctn.grid(column=0, sticky="we")
        self.video.pack()
        self.start_recording_btn.pack()
        self.stop_recording_btn.pack()

        #components event binding
        self.root.bind('<Escape>', lambda e: self.root.quit())

    def close_video(self):
        VideoCamera.capture_object.release()
        cv2.destroyAllWindows()
        self.video.configure(image="")

    def close_app(self):
        VideoCamera.close = True
        self.stop_camera()
        self.root.quit()
        self.root.destroy()
        exit(0)

    def run_camera(self):
        print("start recording...")
        VideoCamera.isRecording = True
        camera_thread = threading.Thread(target=self.show_frame)
        camera_thread.start()
        self.stop_recording_btn.configure(state="normal")
        self.start_recording_btn.configure(state="disabled")

    def stop_camera(self):
        print("stop recording...")
        VideoCamera.isRecording = False
        self.stop_recording_btn.configure(state="disabled")
        self.start_recording_btn.configure(state="normal")
        self.close_video()

    def show_frame(self):
        VideoCamera.capture_object = cv2.VideoCapture(0)
        VideoCamera.capture_object.set(cv2.CAP_PROP_FRAME_WIDTH, self.video_width)
        VideoCamera.capture_object.set(cv2.CAP_PROP_FRAME_HEIGHT, self.video_height)
        while VideoCamera.isRecording:
            try:
                _, VideoCamera.frame = VideoCamera.capture_object.read()
                VideoCamera.frame = cv2.flip(VideoCamera.frame, 1)
                VideoCamera.frame = Image.fromarray(VideoCamera.frame)
                imgtk = ImageTk.PhotoImage(image=VideoCamera.frame)
                self.video.configure(image=imgtk)
            except:
                pass
            if VideoCamera.close:
                break
                exit(0)
        if VideoCamera.close:
                exit(0)
    
    def run(self):
        self.root.mainloop()



if __name__ == "__main__":
    app = VideoCamera()
    app.run()

#imgtk = cv2.resize(imgtk, (533, self.win_height), interpolation = cv2.INTER_AREA)