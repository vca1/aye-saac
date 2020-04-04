
import cv2
import time
from pprint import pprint

from ayesaac.services_lib.queues.queue_manager import QueueManager
from ayesaac.services_lib.images.crypter import encode


class WebCamBis(object):
    """
    The class WebCamBis goal is to take a picture and send it back to CameraManager.
    It's a duplicate from WebCam class, it will be replace by a Kinect class in the future.
    """

    def __init__(self):
        self.queue_manager = QueueManager([self.__class__.__name__, 'CameraManager'])

    def callback(self, body, **_):
        # avoid conflict over opencv between WebCam class
        time.sleep(2)

        cap = cv2.VideoCapture(0)
        _, image = cap.read()
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image = cv2.resize(image, (640, 480), cv2.INTER_AREA)
        pprint(image.shape)
        body['picture'] = {'data': encode(image), 'shape': image.shape, 'from': self.__class__.__name__}
        self.queue_manager.publish('CameraManager', body)

    def run(self):
        self.queue_manager.start_consuming(self.__class__.__name__, self.callback)


def main():
    web_cam_bis = WebCamBis()
    web_cam_bis.run()


if __name__ == '__main__':
    main()
