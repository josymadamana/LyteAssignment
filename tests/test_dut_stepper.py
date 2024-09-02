import logging
import pytest
from config.test import STEPPER_TEST_CONFIG, get_config_args
logger = logging.getLogger("LyteProject")
DEVICE_CONTROL_TOPIC = 'lyte/devicecontrol'


class TestDUTStepper:

    @pytest.mark.parametrize("parameters",
                             get_config_args(file=STEPPER_TEST_CONFIG, config_name="gpio_high_toggle_count"))
    def test_gpio_high_toggle_count_on_rotation(self, dut_monitor, dut_mqtt, parameters):
        """Tests the DUT is toggling GPIO based on the rotation it performs.
        :param dut_monitor: Fixture to monitor DUT
        :param dut_mqtt: Fixture to send MQTT messages to DUT
        :return:
        """
        angle = parameters["angle"]
        count = parameters["count"]
        logger.info(f"Test angle: {angle}, count: {count}")

        # Start Arduino based DUT GPIO monitoring thread
        dut_monitor.start()
        response = dut_mqtt.send_mqtt_request(topic=DEVICE_CONTROL_TOPIC,
                                              msg=str({"device":'stepper', "value": angle}), timeout_s=60)
        logger.info(f"Response received: {response}")
        assert f"{DEVICE_CONTROL_TOPIC}/response/ack" == response, "Test failed. Received NACK from DUT"

        # Stop Arduino based DUT GPIO monitoring thread
        dut_monitor.stop()
        dut_monitor.join()

        # Compare expected count vs monitored count
        assert count == dut_monitor.gpio_high_toggle_count, \
            f"GPIO high toggle count {dut_monitor.gpio_high_toggle_count} is incorrect"

    @pytest.mark.parametrize("parameters",
                             get_config_args(file=STEPPER_TEST_CONFIG, config_name="gpio_final_status"))
    def test_gpio_final_status_after_rotation(self, dut_monitor, dut_mqtt, parameters):
        """Tests the DUT GPIO state is correct after it toggles GPIO based on the rotation it performs.
        :param dut_monitor: Fixture to monitor DUT
        :param dut_mqtt: Fixture to send MQTT messages to DUT
        :return:
        """
        angle = parameters["angle"]
        status = parameters["status"]
        logger.info(f"Test angle: {angle}, status: {status}")

        # Send MQTT msg to DUT
        response = dut_mqtt.send_mqtt_request(topic=DEVICE_CONTROL_TOPIC,
                                              msg=str({"device":'stepper', "value": angle}), timeout_s=60)
        logger.info(f"Response received: {response}")

        assert f"{DEVICE_CONTROL_TOPIC}/response/ack" == response, "Test failed. Received NACK from DUT"
        assert status == dut_monitor.read_gpio_status(), "GPIO final status is incorrect"
