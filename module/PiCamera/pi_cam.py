# module specific includes

import time
from time import strftime, localtime
from picamera import PiCamera


class PiCam:
    def __init__(self, **kwargs):
        pass

    def set_param(self, k, v):
        pass

    def timed_record(self, time):
        pass


class PiCamV1_3(PiCam):
    """
    Class PiCamV1_3 -> Revision 1.3
    The main class that has been built for the PiCamera revision 1.3. using Python 3.7

    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera = PiCamera()

        # defined_settings are the settings that are currently implemented with their own validation of camera input.
        # This means that other settings can be accessible but don't have any level of validation a.k.a no idea if they
        # Truly work as expected.
        self.defined_settings = {
            'resolution': self.set_resolution,
            'brightness': self.set_brightness,
            'contrast': self.set_contrast,
            'iso': self.set_iso,

        }

        self.unsupported_settings = ['stereo_decimate',
                                     'stereo_mode']  # Unable to test, so these settings are blacklisted.

        self.local_settings = {
            'video_lock': False,
            # video lock is to determine if the resolution can be recorded or needs to be captured.
        }
        self.video_resolutions = list()

        for k, v in kwargs.items():
            self.set_param(k, v)

    def __getattr__(self, item):
        if hasattr(self, item):
            return self[item]
        if hasattr(self.camera, item):
            return self.camera[item]

    @staticmethod
    def generate_path(prefix, extension):
        return prefix + time.strftime("%m-%d-%H:%M:%S") + extension

    def set_iso(self, iso):
        """The set_iso function is used to store an iso value to the camera.
        The function call will also show the filtering of ISO values."""

        """ The V2 Camera has different calculation with grain.
        Contrary to the V1.3 it follows the ISO film speed standard. 
        Given that it is more likely that different camera's or other ISO readings can be used externally,
        it is preferabble to use a standard rather than a propriatery calculation.       
        """

        self.camera.iso = iso * 0.0184  # the multiplication to get the ISO standard grain with v1.3 camera.
        pass

    def set_param(self, k, v):
        """
        :param k: String, the key that contains the name of the setting
        :param v: Mixed, the value associated with the key
        :return: Bool, True if storing has succeeded, False if attribute wasn't stored.
        """
        """ I've opted not to attempt implementing all the different unique features.
        The reason for this is because I've counted well over 400 features."""

        if k in self.defined_settings.keys():
            return self.defined_settings[k](v)
        if k in self.unsupported_settings:
            print('SETTING CAN NOT BE CONFIGURED')
            return False
        else:
            setattr(self.camera, k, v)  # I can imagine new functions will be implemented without needing
            # It's own validation, therefore I will implement a default behaviour call.
        return True

    def timed_record(self, recording_seconds=10):
        """
        This function records a video. The file is saved as a .h264 file with the name vid(moment of video taken)
        :param recording_seconds: Time in seconds that will be recorded
        :return:
        """
        self.camera.start_recording("vid" + strftime("%m-%d-%H:%M:%S", localtime()) + ".h264", quality=100)
        self.camera.wait_recording(recording_seconds)
        self.camera.stop_recording()

    def manual_capture(self, output, format=None, use_video_port=False, resize=None, splitter_port=0, bayer=False,
                       **options):

        """Function that captures a full rolling shutter frame.
        The API functionality is implemented, but actually documenting usage is out of scope at the moment.
        Recommended read: https://picamera.readthedocs.io/en/latest/api_camera.html#picamera.PiCamera.capture
        """

        self.camera.capture(output, format=None, use_video_port=False, resize=None, splitter_port=0, bayer=False,
                            **options)

    def capture(self):
        """
        Function to capture a single frame. Basic implementation of the manual_capture.
        :return:
        """
        self.manual_capture(self.generate_path("pic", ".jpg"))

    def instantiate_resolutions(self):
        # TODO Add docs
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

        for i in range(1, len(allowed_video_resolutions)):
            param = {
                'width': allowed_video_resolutions[i][0],
                'height': allowed_video_resolutions[i][1],
                'aspect_frame_rate_min': allowed_frame_rates_ranges[i][0],
                'aspect_frame_rate_max': allowed_frame_rates_ranges[i][1],
            }
            self.video_resolutions.append(VideoResolution(param))

    def set_resolution(self, x, y):
        """
        Changes the resolution of the PiCamera
        :param x: amount of pixels for x
        :param y: amount of pixels for y
        :return:
        """
        self.camera.resolution = (x, y)

    def set_brightness(self, value):
        """
        Set the contrast of the camera valuing from 0-100
        :param value: given brightness value from 0-100
        """
        self.camera.brightness = value

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

        return self.local_settings

    def set_contrast(self, value):
        """
        Set the contrast of the camera valuing from 0-100
        :param value: given contrast value from 0-100
        """
        self.camera.contrast = value

    def get_contrast(self):
        """
        Returns the current contrast of the camera
        :return: contrast value
        """
        return self.camera.contrast


class VideoResolution:
    """The VideoResolution class is responsible for storing a video resolution option
    As is described on the wiki, the rolling shutter introduces a series of challenges.
    A rolling shutter can prevent the camera from recording or taking a sequence of pictures with pauses in between.
    The VideoResolution class will store a singular option of a resolution.
    """

    def __init__(self, **kwargs):
        """
        The constructor instantiate a series of variables that are assigned via key value.
        Checks will need to be introduced individually
        :param kwargs: key value arguments that are set via setattr()
        """
        """In order to make v"""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def is_resolution(self, width, height):
        """
        Validation if the param
        :param width: the resolutions width (e.g. 1920)
        :param height: the resolution height (e.g. 1080)
        :return:
        """
        if self.width is width and self.height is height:
            return True
        return False

    @staticmethod
    def calculate_aspect_ratio(width, height):
        """The calculate aspect ration function is pretty self-explanatory,
        Calculates the aspect ratio it and returns it

        :param width: horizontal width
        :param height: vertical height
        :return: tuple of aspect ratio elements
        """

        pass

    def valid_frame_rate(self, fps):
        """
        Validates if a given FPS is allowed within the range of a resolution
        :param fps: frames per second expected to set.
        :return: Bool, true if valid, false if invalid
        """
        if self.aspect_frame_rate_min <= fps < self.aspect_frame_rate_max:
            return True
        return False

    def validate(self, width, height, fps):
        """
        Validates if the settings coincide with a video resolution instance
        :param width: resolution width
        :param height: resolution height
        :param fps: target FPS
        :return: Bool, True if all checks validated, False if one or more checks failed
        """
        return True is self.valid_frame_rate(fps) and self.is_resolution(width, height)


class PiCamV2(PiCamV1_3):
    """The PiCamV2 is similar to the revision 1.3 and has been made the correct the differences.
    To clarify what differences mean, some functions have been overridden to cause the same or similar result as the 1.3
    To the future user of this module, I recommend testing it thoroughly, I didn't get a chance to get a V2 version.
    """

    def set_iso(self, value):
        self.camera.iso = value  # Doesn't require a different verification due to factory calibration.


class PiCameraConfigurationHandler:
    def __init__(self):
        pass


def pi_camera_factory(**kwargs):
    """ The pi_camera_factory is a simple function that will instantiate the desired camera class
    based on the connected camera. Keep in mind that is done via differentiating the revision that the hardware returns.
    Having a copy camera that does not adhere to same lens, might pose an issue when instantiating.
    Furthermore, keep in mind that the currently factory only works when ONE camera is connected.
    I am unaware of anyway to connect a second camera to single Pi,
    however there are stereoscopic modes that indicate it should be possible.
    The original developer of the picamera library has also indicated that those capabilities haven't been tested."""
    if PiCamera.revision == 'ov5647':  # PiCam Revision 1.3
        return PiCamV1_3(**kwargs)
    if PiCamera.revision == 'IMX219':  # PiCam Revision 2.x
        return PiCamV2(**kwargs)
