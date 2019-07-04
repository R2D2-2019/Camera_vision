import io
import logging
import socketserver
from http import server
from threading import Condition

from modules.rgb_camera.module.PiCamera.outputs.stream import BaseDataStream


class StreamingDataStream(BaseDataStream, object):
    """Streaming data stream is a class that is specially used for storing MJPEG images for streaming purposes"""

    def __init__(self):
        super().__init__()
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


class StreamingHandler(server.BaseHTTPRequestHandler):
    """Streaming Handler is the class that is responsible for actual HTTP request management on the PI
    Future implementation would switch this to the Server.
    Recommended to know the frequent HTTP codes, 200, 301, 404."""
    html_entity = """
                    <html>
                    <head>
                    <title>PICAMERA</title>
                    </head>
                    <body>
                    <img src="stream.mjpg" width="640" height="480" />
                    </body>
                    </html>
                  """
    # HTML entity is the actual page that gets rendered
    output = None  # Output that the camera delivers.

    def add_output(self, output):
        """ The output needs to be added manually. This allows hot swap stream switching."""
        self.output = output

    def do_GET(self):  # GET has been placed instead of get, to imply it is a HTTP GET call.
        if self.path == '/':
            self.send_response(
                301)  # We will be redirecting so a 301 is in order.
            self.send_header('Location',
                             '/index.html')  # We want to redirect all traffic to our dedicated endpoint,
            self.end_headers()
        elif self.path == '/index.html':  # Basic display of the page of the HTML entity page
            content = self.html_entity.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':  # If you only want the actual stream, you can just call the stream mjpg path.
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with self.output.condition:
                        self.output.condition.wait()
                        frame = self.output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)  # Some tried to access a specific endpoint that doesn't excises. 404 in order.
            self.end_headers()
            # We're not redirecting to index.html, because this will just cause a performance hit of multiple visitors


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    """Streaming server is responsible for engaging the HTTP access point.
    A specific port can be assigned which will enable the Streaming Handler to be accessible via IP.
    Usage is simply:

    An address with an appended port in a tuple, example: ('', 9876), will assign it to localhost at port 9876

    An actual StreamingHandler instance

    Example class call StreamingServer(address, StreamingHandler(output))
    """
    allow_reuse_address = True
    daemon_threads = True
