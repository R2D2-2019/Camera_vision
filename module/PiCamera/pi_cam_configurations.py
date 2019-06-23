class BasePiCameraConfiguration:
    def __init__(self):
        """ BasePiCameraConfiguration class contains all the required functions to use a specified configuration"""
        self.settings = dict()  # Used to store the settings.

    def set_settings(self, other):
        """
        Stores settings to a picamera class.
        :param other: PiCamera class, used for setting the attributes directly.
        :return:
        """
        for key, value in self.settings.items():
            if value is not None:
                setattr(other, key, value)

    def apply(self, pi_camera_instance):
        """
        Applies the pi configuration to a pi camera instance via the set_param calls
        :param pi_camera_instance:
        :return:
        """
        for k, v in self.settings.items():
            pi_camera_instance.set_param(k, v)


class LowLightCameraConfiguration(BasePiCameraConfiguration):
    """The basic configuration that uses the low light options that the camera permits.
    Recommend reading through the entire conversation: https://github.com/waveform80/picamera/issues/323
    """

    def __init__(self):
        super().__init__()
        """
        Function which enables low lightning capture to take pictures/videos when it dark.
        :return:
        """
        self.settings = {
            'framerate': 20,
            'exposure_mode': 'nightpreview',
            'exposure_compensation': 25,
        }


class DefaultConfiguration(BasePiCameraConfiguration):
    """The default configuration of the pi camera."""
    """
    Sets most camera settings to various default values.
    """

    def __init__(self):
        super().__init__()
        self.settings = {
            '_exif_tags': {
                'IFD0.Model': 'RP_%s' % 'revision',
                'IFD0.Make': 'RaspberryPi',
            },
            'sharpness': 0,
            'contrast': 0,
            'brightness': 50,
            'saturation': 0,
            'iso': 0,
            'video_stabilization': False,
            'exposure_compensation': 0,
            'exposure_mode': 'auto',
            'meter_mode': 'average',
            'awb_mode': 'auto',
            'image_effect': 'none',
            'color_effects': None,
            'rotation': 0,
            'hflip': False,
            'vflip': False,
            'zoom': (0.0, 0.0, 1.0, 1.0)
        }


class CustomPiCameraConfiguration(BasePiCameraConfiguration):
    """Although it isn't the nicest approach, it would be preferable to update the camera configuration on the fly"""

    def __init__(self, **kwargs):
        super().__init__()

        self.settings = dict()
        for k, v in kwargs.items():
            self.settings.k = v
            setattr(self, k, v)


class CameraConfigurator:
    """Container for managing and assigning the different camera configurations."""

    def __init__(self):
        """ Initialises the configurations that are present."""
        self.configuration = [DefaultConfiguration(), LowLightCameraConfiguration(), CustomPiCameraConfiguration()]

    def apply_configuration(self, configuration_id, pi_camera_instance):
        """
        :param configuration_id: the unique identifier of the configuration that is requested
        :param pi_camera_instance: an instance of the PiCam NOT THE PICAMERA IT SELF.
        :return:
        """

        if configuration_id in range(0, len(self.configuration)):
            self.configuration[configuration_id].apply(pi_camera_instance)
