from client.comm import BaseComm
from common.frame_enum import FrameType
from abc import ABC


class Webcam(ABC):
    def __init__(self, comm: BaseComm):
        self.comm = comm
        # self.comm.listen_for([FrameType.BUTTON_STATE])

    def capture(self):
        pass

    def record(self):
        pass

    def set_resolution(self, x, y):
        pass

    def process(self):
        pass

    def stop(self):
        pass
