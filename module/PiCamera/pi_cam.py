# module specific includes

import time
from time import strftime, localtime
from picamera import PiCamera


class PiCam:
    def __init__(self, **kwargs):
        self.camera = PiCamera()

        # defined_settings are the settings that are currently implemented with their own validation of camera input.
        # This means that other settings can be accessible but don't have any level of validation a.k.a no idea if they
        # Truly work as expected.
        self.defined_settings = {'set_resolution', self.set_resolution}

        self.unsupported_settings = ['stereo_decimate',
                                     'stereo_mode']  # Unable to test, so these settings are blacklisted.

        # Once might argue that storing these values in an attribute would be a better approach.
        # The problem that might arise is naming conflicts, it's easier to know who handles what based on a prefix.
        self.local_settings = {}

        self.video_resolutions = list()  # Depending on the camera, there are multiple video_resolutions possible.

        self.instantiate_resolution()  # Instantiating the possible resolutions so that validation can commence.

    def register_video_resolution(self, resolution):
        self.video_resolutions.append(resolution)

    @staticmethod
    def generate_path(prefix, extension):
        return prefix + time.strftime("%m-%d-%H:%M:%S") + extension

    def set_param(self, k, v):
        """
        :param k: String, the key that contains the name of the setting
        :param v: Mixed, the value associated with the key
        :return: Bool, True if storing has succeeded, False if attribute wasn't stored.
        I've opted not to attempt implementing all the different unique features.
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

    def timed_record(self, output=None, recording_seconds=10):
        """
        This function records a video. The file is saved as a .h264 file with the name vid(moment of video taken)
        :param output: a Data Stream instance, if left None a .h264 video file will be generated.
        :param recording_seconds: Time in seconds that will be recorded
        :return: String that contains the time when the stream was started.
        This can be used to either locate the video, serve as a log or be ignored entirely.
        """
        start_time = strftime("%m-%d-%H:%M:%S", localtime())
        if not output:
            output = self.generate_path("vid", ".h264")
        self.camera.start_recording(output, quality=100)
        self.camera.wait_recording(recording_seconds)
        self.camera.stop_recording()
        return start_time

    def manual_capture(self, output, format=None, use_video_port=False, resize=None, splitter_port=0, bayer=False,
                       **options):
        """Function that captures a full rolling shutter frame.
        The API functionality is implemented, but actually documenting usage is out of scope at the moment.
        Recommended read: https://picamera.readthedocs.io/en/latest/api_camera.html#picamera.PiCamera.capture
        """
        self.camera.capture(output, format=None, use_video_port=False, resize=None, splitter_port=0, bayer=False,
                            **options)

    def set_resolution(self, x, y, nearest=False):
        """
        Changes the resolution of the PiCamera. Not all resolutions allow recording
        Based on the resolutions filtering will be applied, however possible resolutions
        :param x: amount of pixels for x
        :param y: amount of pixels for y
        :param nearest: set the video resolution if not find the nearest. Will always result in video lock false.
        :return: Bool, True if the resolution can be recorded, False if resolution set but no video.
        """
        if nearest:
            x, y = PiCamera.PiResolution(x, y).pad()  # returns an tuple with x and y coordinates.

        for vid_res in self.video_resolutions:
            if vid_res.is_resolution(x, y):
                self.camera.resolution = (x, y)
                self.local_settings.video_lock = False
                self.local_settings.video_resolution = vid_res
                return True

        self.local_settings.video_resolution = None
        self.local_settings.video_lock = True
        self.camera.resolution = (x, y)
        return False

    def instantiate_resolution(self):
        pass


class PiCamV13(PiCam):
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
            'brightness': self.set_brightness,
            'contrast': self.set_contrast,
            'iso': self.set_iso,
        }

        # Once might argue that storing these values in an attribute would be a better approach.
        # The problem that might arise is naming conflicts, it's easier to know who handles what based on a prefix.
        self.local_settings = {
            'video_lock': False,
            # video lock is to determine if the resolution can be recorded or needs to be captured.
            'video_resolution': None  # Storing the pre-defined video resolutions.
        }

        self.video_resolutions = list()  # Each camera has a limited amount of video resolutions.
        # The resolutions are stored to use later on.

        for k, v in kwargs.items():
            self.set_param(k, v)

    def __getattr__(self, item):
        if hasattr(self, item):
            return self[item]
        if hasattr(self.camera, item):
            return self.camera[item]

    def set_iso(self, iso):
        """The set_iso function is used to store an iso value to the camera.
        The function call will also show the filtering of ISO values.
        The V2 Camera has different calculation with grain.
        Contrary to the V1.3 it follows the ISO film speed standard.
        Given that it is more likely that different camera's or other ISO readings can be used externally,
        it is preferable to use a standard rather than a proprietary calculation.
        source: https://picamera.readthedocs.io/en/latest/api_camera.html?highlight=iso#picamera.PiCamera.iso

        The PiCameraV2
        :param iso: integer: the new iso value that will be set.
        The ISO value must be in a possible range, if not the nearest will be selected.
        :return iso: the actual set value of ISO.
        the actual return value will always be different due to the grain calculation.
        In normal circumstances won't be useful. Therefore the return is conditional.
        """

        possible_iso_range = [100, 200, 320, 400, 500, 640, 800]  # The camera has limited amount of ISO values.
        if iso not in possible_iso_range:
            iso = min(possible_iso_range, key=lambda x: abs(x - iso))  # lambda that finds nearest value and sets to iso
        self.camera.iso = iso * 0.0184  # the multiplication to get the ISO standard grain with v1.3 camera.

    def capture(self):
        """
        Function to capture a single frame. Basic implementation of the manual_capture.
        :return:
        """
        self.manual_capture(self.generate_path("pic", ".jpg"))

    def instantiate_resolutions(self):
        """Instantiating the video resolutions that the PiCam V1.3 supports.
        Source: https://picamera.readthedocs.io/en/latest/fov.html#sensor-modes"""
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

    def set_brightness(self, value):
        """
        Set the brightness of the camera valuing from 0-100
        Can be updated during operations.
        Default value is 50
        :param value: given brightness value from 0-100
        """
        if value in range(0, 100):
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
        Can be done during operations running.
        :param value: given contrast value from 0-100
        """

        if value in range(0, 100):
            self.camera.contrast = value

    def get_contrast(self):
        """
        Returns the current contrast of the camera
        :return: contrast value
        """
        return self.camera.contrast


class PiCamV21(PiCamV13):
    """The PiCamV21 is similar to the revision 1.3 and has been made the correct the differences.
    To clarify what differences mean, some functions have been overridden to cause the same or similar result as the 1.3
    To the future user of this module, I recommend testing it thoroughly, I didn't get a chance to get a V2.1 version.
    """

    def instantiate_resolutions(self):
        """Instantiating the video resolutions that the PiCam V2.1 supports.
        Source: https://picamera.readthedocs.io/en/latest/fov.html#sensor-modes"""
        allowed_video_resolutions = [
            ['1920', '1080'],
            ['3280', '2464'],
            ['1640', '1232'],
            ['1640', '922'],
            ['1280', '720'],
            ['640', '480'],
        ]
        allowed_frame_rates_ranges = [
            [0.1, 30],
            [0.1, 15],
            [0.1, 40],
            [0.1, 40],
            [40, 90],
            [40, 90],
        ]

        for i in range(1, len(allowed_video_resolutions)):
            params = {
                'width': allowed_video_resolutions[i][0],
                'height': allowed_video_resolutions[i][1],
                'aspect_frame_rate_min': allowed_frame_rates_ranges[i][0],
                'aspect_frame_rate_max': allowed_frame_rates_ranges[i][1],
            }
            self.register_video_resolution(VideoResolution(params))

    def set_iso(self, value):
        self.camera.iso = value  # Doesn't require a different verification due to factory and standard calibration.


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
        return PiCamV13(**kwargs)
    if PiCamera.revision == 'IMX219':  # PiCam Revision 2.x
        return PiCamV21(**kwargs)
