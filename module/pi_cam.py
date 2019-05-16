import webcam
from picamera import PiCamera


class PiCam():
    """Class for the PiCam"""
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (1280, 720)

    def record(self, time):
        """
        this function takes a time in seconds and records to the
        filename that is specified ...
        """

        self.camera.start_preview()
        self.camera.start_recording("testfile.mjpeg", quality=30)
        self.camera.wait_recording(time)
        self.camera.stop_recording()
        self.camera.stop_preview()


print("starting camera...")
my_camera = PiCam()
my_camera.record(10)

print("done...")
