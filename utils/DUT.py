#!/usr/bin/env python3
""" To simulate DUT MQTT server
"""
import paho.mqtt.client as mqtt
import json
import os
import logging
from datetime import datetime
from libs.steppercontrol import Stepper
logger = logging.getLogger(__name__)
LOG_PATH = os.path.join(os.path.dirname(__file__), 'logs')
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)
TEST_LOG_FILENAME = os.path.join(LOG_PATH, f"DUT_log-{datetime.now().strftime('%Y-%m-%d')}.log")

logging.basicConfig(filename=TEST_LOG_FILENAME, encoding='utf-8', level=logging.DEBUG,
                    format='[%(asctime)s] [%(pathname)s:%(lineno)d] [%(levelname)s]  %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

MQTT_SERVER = "localhost"
MQTT_PATH = "lyte/devicecontrol"
stepper = Stepper()

class DUT:
    def __init__(self, mqtt_port=1883, keepalive=60):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(MQTT_SERVER, mqtt_port, keepalive)

    def loop(self):
        self.client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        logger.info("Connected with result code " + str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.client.subscribe(MQTT_PATH)

    def move_stepper(self, angle, client):
        # Start the rotation
        # if angle is multiple of 180; call toggle_gpio(STEPPER_GPIO_PIN)
        response_topic = f"{MQTT_PATH}/response"
        if stepper.move_at_angle_with_gpio_toggle(angle_in_degree=angle):
            self.client.publish(topic=f"{response_topic}/ack")
        else:
            self.client.publish(topic=f"{response_topic}/nack")
        logger.info("move_stepper response sent")

    def on_message(self, client, userdata, msg):
        try:
            json_payload = json.loads(msg.payload.decode('utf8').replace("'", '"'))
        except ValueError:
            logger.error(f"Unable to parse JSON payload from {msg.payload} for TOPIC:{msg.topic}")
            return

        if msg.topic == MQTT_PATH:
            if json_payload.get("device") == "stepper":
                logger.info(f"Stepper going to be rotated by {json_payload['value']}")
                try:
                    self.move_stepper(int(json_payload['value']), client)
                except ValueError:
                    logger.error(f"Unable to move stepper to {json_payload['value']}. Not an integer angle")

            elif json_payload.get("device") == "led":
                logger.info(f"LED going to be set to {json_payload['value']}")
                if json_payload['value'] == "on":
                    logger.info("Turning On LED")
                    # GPIO.output(LED_PIN, GPIO.HIGH)
                elif json_payload['value'] == "off":
                    logger.info("Turning Off LED")
                    # GPIO.output(LED_PIN, GPIO.LOW)
                else:
                    logger.warning(f"Received unsupported value for LED device. TOPIC: {msg.topic}, PAYLOAD: {msg.payload}")

            else:
                logger.warning(f"Received unsupported device. TOPIC: {msg.topic}, PAYLOAD: {msg.payload}")
        else:
            logger.warning(f"Received unsupported message. TOPIC: {msg.topic}, PAYLOAD: {msg.payload}")


if __name__ == "__main__":
    dut = DUT()
    dut.loop()