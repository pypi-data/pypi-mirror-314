import random

import paho.mqtt.client as mqtt_client

"""
Library documentation: https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php
"""


def _on_connect(client, userdata, flags, rc):
    print("client:", client, "userdata:", userdata, "flags:", flags, "code:", rc)
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect")


def _on_disconnect(client, userdata, rc):
    print("client:", client, "userdata:", userdata, "code:", rc)
    print("Unexpected disconnection.")


def _on_log(client, userdata, level, buf):
    print("client:", client, "userdata:", userdata, "level:", level, "buf", buf)


class MQTTClient:

    def __init__(self, broker, port) -> None:
        super().__init__()

        self.broker = broker
        self.port = port
        print("starting mqtt client, broker:", broker, "port:", port)

        client_id = f'python-mqtt-{random.randint(0, 1000)}'
        self.client = mqtt_client.Client(client_id)

    def connect_safe(self, username, password):
        self.client.username_pw_set(username, password)
        self.connect()

    def connect(self):
        self._set_callbacks()
        self.client.connect(host=self.broker, port=self.port)

    def disconnect(self):
        self.client.disconnect()

    def _set_callbacks(self):
        self.client.on_connect = _on_connect
        self.client.on_disconnect = _on_disconnect
        # self.client.on_log = _on_log

    def subscribe(self, topic, callback):
        """
        example of a callback:
        def callback(client, userdata, msg):
             print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        """
        self.client.on_message = callback
        self.client.subscribe(topic)

    def subscribe_many(self, topics: list[str], callback):
        topic_array = []
        for t in topics:
            topic_array.append((t, 0))
        self.subscribe(topic=topic_array, callback=callback)

    def publish(self, topic, data):
        result = self.client.publish(topic, data)
        status = result[0]
        if status == 0:
            print(f"Send `{data}` to topic `{topic}`")
            return True
        else:
            print(f"Failed to send message to topic {topic}")
            return False

    def loop_forever(self):
        self.client.loop_forever()

    def loop_start(self):
        self.client.loop_start()

    def loop_stop(self):
        self.client.loop_stop(force=True)


# ----------------------------------------------------------------------------------------
# EXAMPLE
# ----------------------------------------------------------------------------------------
'''
import json

def callback(client, userdata, msg):
    try:
        _data = json.loads(msg.payload.decode())
        print(_data)
    except Exception as e:
        print("Error:", userdata, msg, str(e))


if __name__ == '__main__':
    mqtt = MQTTClient(broker=BROKEN_MQTT, port=BROKEN_MQTT_PORT)
    while True:
        mqtt.connect()
        mqtt.loop_start()
        mqtt.subscribe_many(topics=load_topics(), callback=callback)
        mqtt.loop_stop()
        mqtt.disconnect()
'''
