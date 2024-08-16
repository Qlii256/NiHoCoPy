import json
import threading

import paho.mqtt.client as mqtt


class Connection(threading.Thread):
    def __init__(self):
        # Create a new MQTT client
        self._client = mqtt.Client()

        # Callbacks
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message

        # Initialize the thread
        super().__init__()

    def connect(self, address: str, port: int, username: str, password: str, certificate: str):
        # Set username and password
        self._client.username_pw_set(username, password)

        # Set the certificate
        self._client.tls_set(ca_certs=certificate)

        # Do no verify IP address on the certificate
        self._client.tls_insecure_set(True)

        # Connect to the server
        self._client.connect(address, port, 60)

        # Actually start the loop to force a connection
        self._client.loop_start()
        while not self._client.is_connected():
            continue

    def start(self):
        # Subscribe to all events
        self.subscribe('hobby/control/devices/rsp')
        self.subscribe('hobby/control/devices/evt')
        self.subscribe('hobby/control/devices/err')

    def stop(self):
        self.close()

    def close(self):
        print(f'Gracefully shutting down')
        self._client.loop_stop()
        self._client.disconnect()

    def subscribe(self, topic: str):
        self._client.subscribe(topic)

    def publish(self, topic: str, data: dict):
        self._client.publish(topic, payload=json.dumps(data))

    def on_message(self, topic: str, data: dict):
        pass

    def _on_message(self, client: mqtt.Client, userdata, message: mqtt.MQTTMessage):
        self.on_message(message.topic, json.loads(message.payload))

    @staticmethod
    def _on_connect(client: mqtt.Client, userdata, flags, result: str):
        if result != 0:
            print(f'Connection failed: {mqtt.error_string(result)}')
        else:
            print(f'Connection succeeded!')


