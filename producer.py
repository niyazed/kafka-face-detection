import time
import sys
import cv2
import base64

from kafka import KafkaProducer
from kafka.errors import KafkaError

producer = KafkaProducer(bootstrap_servers='localhost:9092')
topic = 'altersense'


def send_video(path_to_video):
    print('start')

    video = cv2.VideoCapture(path_to_video)

    while video.isOpened():
        success, frame = video.read()
        if not success:
            break

        # Encoding part
        data = cv2.imencode('.jpeg', frame)[1].tobytes()
        # data = base64.b64encode(data)

        future = producer.send(topic, data)
        try:
            future.get(timeout=10)
        except KafkaError as e:
            print(e)
            break

        print('.', end='', flush=True)


send_video(0)
