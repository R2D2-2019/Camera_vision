from picamera import PiCamera
import time
from fractions import Fraction


class PiCam:
    """
    Picam class
    Default resolution = 1280 by 720
    """
    brightness = 50
    contrast = 50

    def __init_(self):
        self.camera = PiCamera()
        self.camera.resolution = (1280, 720)
        time.sleep(2)

    # def __init__(self, comm: BaseComm):
    #    self.comm = comm
    #    # self.comm,listen_for([FrameType.tobeadded])
    #    self.camera = PiCamera()
    #    self.camera.resolution = (1280, 720)
        # Warm up camera
    #    time.sleep(2)

    # def process(self):
    #    while self.comm.has_data():
    #        frame = self.comm.get_data()

    #       if frame.request:
    #            continue

    #        values = frame.get_data()

    # def stop(self):
    #    self.comm.stop()

    def record(self, time):
        """
        This function records a video. The file is saved as a .mpeg file with the name vid(moment of video taken)
        :param time: Time in seconds
        :return:
        """
        timestr = "vid" + time.strftime("%m-%d-%H:%M:%S") + ".mpeg"

        self.camera.start_preview()
        self.camera.start_recording(timestr, quality=30)
        self.camera.wait_recording(time)
        self.camera.stop_recording()
        self.camera.stop_preview()

    def capture(self):
        # Gotta add in that filename has date/time in it
        """
        Function to capture a single frame. The file is saved as a .jpg file with the name pic(moment of video taken)
        :return:
        """
        timestr = "pic" + time.strftime("%m-%d-%H:%M:%S") + ".jpg"
        self.camera.capture(timestr)

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
        timestr = "pic" + time.strftime("%m-%d-%H:%M:%S") + ".jpg"
        self.camera.framerate = Fraction(1, 6)
        self.camera.sensor_mode = 3
        self.camera.shutter_speed = 6000000
        self.camera.iso = 800
        # give it a long sleep to gain all the light
        time.sleep(30)
        self.camera.exposure_mode = 'off'
        self.camera.capture(timestr)
        # return settings back to normal
        self.camera.framerate = 30
        self.camera.sensor_mode = 0
        self.camera.shutter_speed = 0
        self.camera.iso = 0
        self.camera.exposure_mode = 'on'

    def set_brightness(self, value):
        """
        Set the contrast of the camera valuing from 0-100
        :param value: given brightness value from 0-100
        """
        self.brightness = value
        self.camera.brightness = self.brightness

    def get_brightness(self):
        """
        Returns the brightness of the camera
        :return: brightness value
        """
        return self.brightness

    def set_contrast(self, value):
        """
        Set the contrast of the camera valuing from 0-100
        :param value: given contrast value from 0-100
        """
        self.contrast = value
        self.camera.contrast = self.contrast

    def get_contrast(self):
        """
        Returns the current contrast of the camera
        :return: contrast value
        """
        return self.contrast
