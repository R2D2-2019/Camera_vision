class BasePiCameraConfiguration:
    def __init__(self):
        self.contrast = None
        self.brightness = None
        self.shutter_speed = None

    def __copy__(self, other):
        for key, value in self.__dict__:
            if value is not None:
                setattr(other, key, value)

    def apply(self, camera):
        self.__copy__(camera)


class LowLightCameraConfiguration(BasePiCameraConfiguration):
    """The basic configuration that uses the low light options that the camera permits."""
    pass


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
        for k, v in kwargs.items():
            setattr(self, k, v)
