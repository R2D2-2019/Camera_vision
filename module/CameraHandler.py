# includes for the python BUS
from client.comm import BaseComm
from common.frame_enum import FrameType


class CameraHandler:
    def __init__(self, comm: BaseComm):
        self.comm = comm
        self.comm.listen_for([FrameType.PLACEHOLDER])  # Implement frametype ASAP!
        # TODO: Define the frame types to listen for
        # TODO: Register the present camera(s)
        pass

    def process(self):
        # TODO: Redirect the present camera to
        pass

    def stop(self):
        self.comm.stop()
