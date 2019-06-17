# module specific includes

import time
from time import strftime, localtime


class PiCamV1:
    """
    Picam class
    Default resolution = 1280 by 720
    """

    def __init__(self, **kwargs):
        self.camera = PiCamera()

        # defined_settings are the settings that are currently implemented with their own validation of camera input.
        # This means that other settings can be accessible but don't have any level of validation a.k.a no idea if they
        # Truly work as expected.
        self.defined_settings = {
            'resolution': self.set_resolution,
            'brightness': self.set_brightness,
            'contrast': self.set_contrast
        }
        self.settings = dict()

        for k, v in kwargs.items():
            self.set_param(k, v)

    def set_param(self, k, v):
        """ I've opted not to attempt implementing all the different unique features.
        The reason for this is because I've counted well over 400 features."""

        if k in self.defined_settings.keys():
            self.defined_settings[k](v)
        else:
            setattr(self.camera, k, v)  # I can imagine new functions will be implemented without needing
            # It's own validation, therefore I will implement a default behaviour call.

    def record(self, time):
        """
        This function records a video. The file is saved as a .mpeg file with the name vid(moment of video taken)
        :param time: Time in seconds
        :return:
        """
        timestr = "vid" + strftime("%m-%d-%H:%M:%S", localtime()) + ".h264"
        self.camera.start_preview()
        self.camera.start_recording(timestr, quality=30)
        self.camera.wait_recording(time)
        self.camera.stop_recording()
        self.camera.stop_preview()

    def capture(self):
        """
        Function to capture a single frame. The file is saved as a .jpg file with the name pic(moment of video taken)
        :return:
        """
        timestr = "pic" + time.strftime("%m-%d-%H:%M:%S") + ".jpg"
        self.camera.capture(timestr)

    def instantiate_resolutions(self):
        allowed_video_resolutions = [
            ['2592', '1944'],
            ['1296', '972'],
            ['1296', '730'],
            ['640', '480'],
            ['640', '480'],
            ['1920', '1080'],
        ]
        allowed_frame_rates_ranges = [
            [1, 15],
            [1, 42],
            [1, 49],
            [42.1, 60],
            [60.1, 90],
            [1, 30]
        ]

    def set_resolution(self, x, y):
        """
        Changes the resolution of the PiCamera
        :param x: amount of pixels for x
        :param y: amount of pixels for y
        :return:
        """

        self.settings.resolution = (x, y)
        self.camera.resolution = self.settings.resolution

    def set_brightness(self, value):
        """
        Set the contrast of the camera valuing from 0-100
        :param value: given brightness value from 0-100
        """
        self.settings.brightness = value
        self.camera.brightness = self.settings.brightness

    def get_brightness(self):
        """
        Returns the brightness of the camera
        :return: brightness value
        """
        return self.camera.brightness

    def get_settings(self):
        """ Returns the dict containing all the settings that have been stored.
        :returns settings dict
        """

        return self.settings

    def set_contrast(self, value):
        """
        Set the contrast of the camera valuing from 0-100
        :param value: given contrast value from 0-100
        """
        self.settings.contrast = value
        self.camera.contrast = self.settings.contrast

    def get_contrast(self):
        """
        Returns the current contrast of the camera
        :return: contrast value
        """
        return self.camera.contrast


def pi_camera_factory():
    # TODO : if picamera.revision > 1:
    return PiCamV1()


class VideoResolution:

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def is_resolution(self, x, y):
        if self.x is x and self.y is y:
            return True
        return False

    def calculate_aspect_ratio(self, a, b):

        pass

    class PiCameraConfigurationHandler:
        def __init__(self):
            pass
