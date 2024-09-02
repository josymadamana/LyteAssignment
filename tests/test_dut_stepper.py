import logging
import json
import pytest
from config.test import STEPPER_TEST_CONFIG, get_config_args
logger = logging.getLogger("LyteProject")
DEVICE_CONTROL_TOPIC = 'lyte/devicecontrol'


class TestDUTStepper:

    @pytest.mark.parametrize("stepper_gpio_high_count_args",
                             get_config_args(file=STEPPER_TEST_CONFIG, config_name="gpio_count"))
    def test_gpio_change_count_on_rotation(self, dut_monitor, dut_mqtt, stepper_gpio_high_count_args):
        """
        :param dut_monitor:
        :param dut_mqtt:
        :return:
        """
        angle = stepper_gpio_high_count_args["angle"]
        count = stepper_gpio_high_count_args["count"]
        logger.info(f"Test angle: {angle}, count: {count}")

        dut_monitor.start()
        response = dut_mqtt.send_mqtt_request(topic=DEVICE_CONTROL_TOPIC,
                                              msg=str({"device":'stepper', "value": angle}), timeout_s=60)
        logger.info(f"Response received: {response}")
        assert f"{DEVICE_CONTROL_TOPIC}/response/ack" == response, "Test failed. Received NACK from DUT"
        dut_monitor.stop()
        dut_monitor.join()
        assert count == dut_monitor.gpio_high_toggle_count, \
            f"GPIO high toggle count {dut_monitor.gpio_high_toggle_count} is incorrect"

    @pytest.mark.parametrize("stepper_gpio_status_args",
                             get_config_args(file=STEPPER_TEST_CONFIG, config_name="gpio_final_status"))
    def test_gpio_final_status_after_rotation(self, dut_monitor, dut_mqtt, stepper_gpio_status_args):
        """
        :param dut_monitor:
        :param dut_mqtt:
        :return:
        """
        angle = stepper_gpio_status_args["angle"]
        status = stepper_gpio_status_args["status"]
        logger.info(f"Test angle: {angle}, count: {status}")

        # Start Arduino monitoring here
        response = dut_mqtt.send_mqtt_request(topic=DEVICE_CONTROL_TOPIC,
                                              msg=str({"device":'stepper', "value": angle}), timeout_s=60)
        logger.info(f"Response received: {response}")
        assert f"{DEVICE_CONTROL_TOPIC}/response/ack" == response, "Test failed. Received NACK from DUT"
        assert status == dut_monitor.read_gpio_status(), "GPIO final status is incorrect"
