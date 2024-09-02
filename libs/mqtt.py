#!/usr/bin/env python3
import time
import logging
logger = logging.getLogger("LyteProject")
from paho.mqtt import client as mqtt_client

class MqttClient:
    """MQTT client lib.
    """
    def __init__(self, host="127.0.0.1", port=1883):
        """DUT in intialize.
        :param host: Broker hostname
        :param port: Broker port
        """
        self.host = host
        self.port = port
        # Generate a Client ID with the publish prefix.
        self.client_id = f'mqtt_client_{time.time()}'
        self.client = self.connect_mqtt()
        self.client.loop_start()
        self.topic_requested = None
        self.topic_response = None

    def connect_mqtt(self):
        """Connect to broker.
        :return:
        """
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                logger.info("Connected to MQTT Broker!")
            else:
                logger.error("Failed to connect, return code %d\n", rc)

        def on_message(client, userdata, msg):
            logger.info(f"Received response: {msg.topic}, {msg.payload}")
            self.topic_response = msg.topic

        client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, self.client_id)
        # client.username_pw_set(username, password)
        client.on_connect = on_connect
        client.connect(self.host, self.port)
        client.on_message = on_message
        return client

    def send_mqtt_request(self, topic, msg, timeout_s=60):
        """Send an MQTT request to the broker.
        :param topic: topic to be published
        :param msg: message to be published
        :param timeout_s: response timeout in seconds
        :return: response topic from the server
        """
        # Send the request message
        self.topic_requested = topic
        self.topic_response = None
        self.client.subscribe(f"{topic}/response/#")
        self.client.publish(topic, msg, qos=2)
        start_time = time.time()
        while time.time() - start_time < timeout_s:
            if self.topic_response is not None:
                break
            time.sleep(1)
        if self.topic_response is None:
            raise f"Response not received for topic:{topic} msg: {msg}"
        else:
            return self.topic_response


    def disconnect(self):
        """Disconnect the MQTT session loop.
        :return:
        """
        self.client.loop_stop()


if __name__ == '__main__':
    mqtt_client = MqttClient(host="127.0.0.1", port=1883)
    mqtt_client.send_mqtt_request(topic='lyte/devicecontrol', msg='{"device":"stepper", "value":360}', timeout_s=60)
    mqtt_client.disconnect()
