from raspi.sensor import sensor_model
from RPi import picamera
# import picamera """ use this on actual rasberry-pi platform """


class CameraSensor(sensor_model.AbstractSensor):

    def is_ok(self):
        return "true"

    def __init__(self, sensor_id, image_file='image1.jpg', video_file='video1.h264'):
        self.image_file = image_file
        self.video_file = video_file
        self.camera = picamera.PiCamera()
        super(CameraSensor, self).__init__(sensor_id)


    def get_ic(self):
        return "camera"

    def get_reading(self):
        self.camera.capture(self.image_file)

    def get_preview(self):
        self.camera.start_preview()

    def start_recording(self):
        self.camera.start_recording(self.video_file)

    def stop_recording(self):
        self.camera.stop_recording(self.video_file)

    def get_image_file(self):
        return self.image_file

    def get_video_file(self):
        return self.video_file
