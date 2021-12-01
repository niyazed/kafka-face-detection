# Realtime face detection using Kafka video streaming 
- Face detection using Kafka | OpenCV | Centerface | Flask
- Running kafka using docker

## Installation
- Install docker, docker-compose
- Install the dependencies:
```python
  $ pip install -r requirements.txt
```
## Kafka & Zookeeper Setup
```
  $ docker-compose -f docker-compose.yml up -d
```
## Finally

- Run kafka producer:
```
  $ python producer.py
```

- And run kafka consumer:
```
  $ python consumer.py
```

Your app should now be running on ***localhost:5000***

## Reference
```
- http://betterdatascience.com/how-to-install-apache-kafka-using-docker-the-easy-way/
- https://github.com/akmamun/kafka-python-camera-stream
```
