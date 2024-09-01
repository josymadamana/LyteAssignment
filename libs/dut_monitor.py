#!/usr/bin/env python3
""" DUT monitor module using Arduino
"""
import logging
import time
from threading import Thread, Event
from libs.arduino import Arduino
logger = logging.getLogger("LyteProject")

class DUTMonitor(Thread):
    """

    """
    def __init__(self, arduino_port="/dev/ttyUSB0", baudrate=115200):
        """

        :param baudrate: Arduino baudrate
        :param arduino_port:
        """
        super().__init__()
        self.arduino = Arduino(arduino_port, baudrate)
        self.gpio_high_toggle_count = 0
        self._stop_event = Event()

    def run(self, timeout=300):
        """

        :param prev_value:
        :return:
        """
        # self.dut_monitor_running = True
        logger.info(f"Monitor thread started")
        self.gpio_high_toggle_count = 0
        start_time = time.time()
        while self.arduino.read_pin_13() != 0 and time.time() - start_time < timeout:
            time.sleep(0.1)
            logger.info(f"reading arduino pin value: {self.arduino.read_pin_13()} until it is 0")
        prev_value = self.arduino.read_pin_13()
        logger.info(f"previous value set as  {prev_value}.")
        if prev_value != 0:
            raise f"DUT did not start with GPIO low. Current value: {prev_value}"
        while not self._stop_event.is_set():
            new_val = self.read_gpio_status()
            if prev_value != new_val:
                prev_value = new_val
                if new_val == 1:
                    self.gpio_high_toggle_count += 1
                    logger.info(f"GPIO high count: {self.gpio_high_toggle_count}")
            time.sleep(0.1)
        logger.info(f"Monitor thread completed")

    def stop(self):
        self._stop_event.set()

    def read_gpio_status(self):
        """

        :return:
        """
        return self.arduino.read_pin_13()

if __name__ == '__main__':
    dut_monitor = DUTMonitor(arduino_port='/dev/ttyUSB0')
    print(f"Latest GPIO status: {dut_monitor.read_gpio_status()}")
    dut_monitor.start()
    start_time = time.time()
    while(time.time() - start_time < 60):
        time.sleep(0.1)
    dut_monitor.stop()
    dut_monitor.join()
    print(f"gpio_high_toggle_count: {dut_monitor.gpio_high_toggle_count}")
    print(f"Latest GPIO status: {dut_monitor.read_gpio_status()}")
