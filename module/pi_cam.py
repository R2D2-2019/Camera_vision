from picamera import PiCamera
from time import sleep


class PiCam:
    """
    Picam class
    Default resolution = 1280 by 720
    """
    def __init__(self, comm: BaseComm):
        self.comm = comm
        # self.comm,listen_for([FrameType.tobeadded])
        self.camera = PiCamera()
        self.camera.resolution = (1280, 720)
        # Warm up camera
        sleep(2)

    def process(self):
        while self.comm.has_data():
            frame = self.comm.get_data()

            if frame.request:
                continue

            values = frame.get_data()

    def stop(self):
        self.comm.stop()

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

    def capture(self):
        """
        Function to capture a single frame
        :return:
        """
        self.camera.capture('test.jpg')

    def set_resolution(self, x, y):
        """
        Changes the resolution of the PiCamera
        :param x: amount of pixels for x
        :param y: amount of pixels for y
        :return:
        """
        self.camera.resolution = (x, y)

    def low_light_capture(self):
        """
        Function which enables low lightning capture to take pictures/videos when it dark.
        :return:
        """
        pass

print("starting camera...")
my_camera = PiCam()
my_camera.record(10)

print("done...")
