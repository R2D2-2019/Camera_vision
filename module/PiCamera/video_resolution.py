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

        # Initialising the default expected variables
        self.width = None
        self.height = None
        self.aspect_frame_rate_min = None
        self.aspect_frame_rate_max = None

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
    def gcd(a, b):
        if b == 0:
            return a
        return VideoResolution.gcd(b, a % b)

    @staticmethod
    def calculate_aspect_ratio(width, height):
        """The calculate aspect ration function is pretty self-explanatory,
        Calculates the aspect ratio it and returns it

        :param width: horizontal width
        :param height: vertical height
        :return: tuple of aspect ratio elements
        """

        divisor = VideoResolution.gcd(1920, 1080)

        x = int(width / divisor)
        y = int(height / divisor)
        return x, y

    def valid_frame_rate(self, fps):
        """
        Validates if a given FPS is allowed within the range of a resolution
        :param fps: frames per second expected to set.
        :return: Bool, true if valid, false if invalid
        """
        return self.aspect_frame_rate_min <= fps < self.aspect_frame_rate_max

    def validate(self, width, height, fps):
        """
        Validates if the settings coincide with a video resolution instance
        :param width: resolution width
        :param height: resolution height
        :param fps: target FPS
        :return: Bool, True if all checks validated, False if one or more checks failed
        """
        return True is self.valid_frame_rate(fps) and self.is_resolution(width, height)
