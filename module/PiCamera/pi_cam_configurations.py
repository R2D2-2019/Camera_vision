class BasePiCameraConfiguration:
    def __init__(self):
        self.settings = dict()
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
    """The default configuration for 'normal' (not too bright not too dim) lighting"""
    pass


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
