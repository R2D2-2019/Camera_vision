class CameraHandler:
    def __init__(self):
        """ Should detect which camera's are present"""
        pass

    def capture(self):
        """ Instructs a camera to take an image"""
        pass

    def process(self):
        while self.comm.has_data():
            frame = self.comm.get_data()

            if frame.request:
                continue

            values = frame.get_data()

            if values[0] == "record":
                self.record(values(1))  # values[1] should hold the time
            else:
                continue  # should add more functionality later?

    def stop(self):
        self.comm.stop()


    def start_recording(self):
        """ Instructs a camera to start recording """
        pass

    def stop_recording(self):
        """ Instructs a camera to stop recording """
        pass

