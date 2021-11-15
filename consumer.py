from flask import Flask, Response
from kafka import KafkaConsumer
import cv2
import base64
import numpy as np
import facedetector


app = Flask(__name__)

consumer = KafkaConsumer('altersense', bootstrap_servers='localhost:9092')


def stream_video():
    for message in consumer:
        # Decoding part
        # data = base64.b64decode(message.value)
        data = np.frombuffer(message.value, dtype=np.uint8)
        frame = cv2.imdecode(data, flags=1)

        # OpenCV Preprocessings
        # grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.flip(frame, 1)
        frame = facedetector.detect(frame)
        frame = cv2.imencode('.jpeg', frame)[1].tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/')
def index():
    return Response(stream_video(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run()