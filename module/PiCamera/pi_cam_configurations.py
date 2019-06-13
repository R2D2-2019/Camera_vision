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
    pass


class


class CustomPiCameraConfiguration(BasePiCameraConfiguration):
    """Although it isn't the nicest approach, it would be preferable to update the camera configuration on the fly"""

    def __init__(self):
        super().__init__()
