#!/usr/bin/env python3
""" Arduino UNO module
"""
import logging
import serial
import os
import time
logger = logging.getLogger("LyteProject")
STX_BYTE = 0x02  # Byte representing the Start Byte of data transmission


class Arduino:
    def __init__(self, port, baudrate=115200):
        """Initialize arduino serial connection.
        :param baudrate: Serial baudrate
        :param port: Serial port
        """
        # DTR reset patch
        os.system(f"sudo stty -F {port} -hupcl")
        time.sleep(2)
        self.arduino = serial.Serial()
        self.arduino.baudrate = baudrate
        self.arduino.port = port
        self.arduino.write_timeout = 1
        self.arduino.timeout = 1
        self.arduino.dsrdtr = False
        try:
            self.arduino.open()
        except serial.SerialException as e:
            logger.error(f"Error opening Arduino serial port: {self.arduino.port}{e}")

    def uninitialize(self):
        """Un-initialize arduino connection.
        :return:
        """
        try:
            self.arduino.close()
        except serial.SerialException as e:
            logger.error(f"Error closing Arduino serial port: {self.arduino.port}{e}")

    def read_pin_13(self):
        """Read pin 13 status.
        :return: A single byte read from the Arduino representing the state of input pin13
        """
        # initialize with start byte
        arduino_msg = [STX_BYTE]
        # 0xfd indicates a serial read of input pin 13
        arduino_msg.append(0xfd)

        try:
            self.arduino.write(arduino_msg)
            return ord(self.arduino.read())
        except serial.SerialException as e:
            raise f"Error reading from Arduino serial port: {self.arduino.port}, {e}"
        except TypeError:
            logger.error("0 bytes read, possible DTR reset on Arduino. "
                         "Execute the following command: sudo stty -F /dev/ttyUSB0 -hupcl")
            raise "0 bytes read, possible DTR reset on Arduino."


if __name__ == '__main__':
    arduino = Arduino(baudrate=115200, port='/dev/ttyUSB0')
    import time
    print(arduino.read_pin_13())
    arduino.uninitialize()
