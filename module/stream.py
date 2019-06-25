import io
import picamera as PiCamera
from threading import Condition


class BaseDataStream:
    """The BaseDataStream class can be used as an abstract class for the output of the PiCamera.
    The Abstract class allows the output to be manipulated or formatted in a way that the library doesn't contain
    The BaseDataStream makes a few assumptions that are described in more detail on the wiki page.
    Keep these in mind during the development.
    """

    def __init__(self):
        """Initialisation of the object, doesn't require any parameters and constructors don't return any either.
        Functions like a normal constructor."""
        pass

    def write(self, buffer):
        """The write function is called by the PiCamera each time an image has been made.
        You can decide to do something with the images (manipulation) or simply store them.
        :param buffer: MemoryStream (io.BytesIO)
        :return: None
        """
        pass

    def flush(self):
        """The flush function is called to signal that PiCamera is done with the a data stream.
        DISCLAIMER: THIS IS NOT RUN BY DEFAULT.
        The flush function will be called when a file is used so an io.BytesIO.
        If you pass in an object of a different type, this function won't be called.
        :return: None
        """
        pass


class StreamingDataStream(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, byte):
        if byte.startswith(b'\xff\xd8'):  # Checking if it's a JPEG image
            self.buffer.truncate()  # Our old buffer is useless, because we get a new one!
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()  # Notifying all threads that we have a new hit.
            self.buffer.seek(0)
        return self.buffer.write(byte)
