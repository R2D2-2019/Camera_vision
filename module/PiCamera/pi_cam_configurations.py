class BasePiCameraConfiguration:
    def __init__(self):
        pass

    def __copy__(self, other):
        for key, value in self.__dict__:
            if value is not None:
                setattr(other, key, value)

    def apply(self, pi_camera_instance):
        for k, v in self.settings:
            pi_camera_instance.set_param(k, v)


class LowLightCameraConfiguration(BasePiCameraConfiguration):
    """The basic configuration that uses the low light options that the camera permits."""

    def __init__(self):
        super().__init__()
        """
        Function which enables low lightning capture to take pictures/videos when it dark.
        :return:
        """

        self.settings = {
            'framerate': 30,
            'exposure_mode': 'off',
            'sensor_mode': '3',
            'shutter_speed': '6000000',
            'iso': '800',
        }


class DefaultConfiguration(BasePiCameraConfiguration):
    """The default configuration of the pi camera."""
    """
    Sets most camera settings to various default values.
    """
    def __init__(self):
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


class AutoConfiguration(BasePiCameraConfiguration):
    """Configuration that will try to use as many auto functions of the camera"""
    pass


class CustomPiCameraConfiguration(BasePiCameraConfiguration):
    """Although it isn't the nicest approach, it would be preferable to update the camera configuration on the fly"""

    def __init__(self, **kwargs):
        super().__init__()

        self.settings = dict()
        for k, v in kwargs.items():
            self.settings.k = v
            setattr(self, k, v)
