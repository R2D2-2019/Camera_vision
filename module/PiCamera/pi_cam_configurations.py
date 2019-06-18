class BasePiCameraConfiguration:
    def __init__(self):
        self.settings = dict()
        pass

    def set_settings(self, other):
        for key, value in self.settings.items():
            if value is not None:
                setattr(other, key, value)

    def apply(self, pi_camera_instance):
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
