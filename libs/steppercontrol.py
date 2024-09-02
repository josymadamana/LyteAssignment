#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import logging
logger = logging.getLogger("LyteProject")
GPIO.setwarnings(False)

in1 = 17
in2 = 18
in3 = 27
in4 = 22
GPIO_TRIGGER_180 = 24
motor_pins = [in1,in2,in3,in4]
# defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]
step_sleep = 0.002  # careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
degree_to_step = 5.625 / 64  # as per the specs


class Stepper:
    def __init__(self):
        """Stepper class init.
        """
        # setting up all pins.
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(in1, GPIO.OUT)
        GPIO.setup(in2, GPIO.OUT)
        GPIO.setup(in3, GPIO.OUT)
        GPIO.setup(in4, GPIO.OUT)
        GPIO.setup(GPIO_TRIGGER_180, GPIO.OUT)

        # initializing
        self.initialize()

    def initialize(self):
        """Initialize all stepper control pins and DUT GPIO.
        :return:
        """
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.LOW)
        GPIO.output(GPIO_TRIGGER_180, GPIO.LOW)
        self.motor_step_counter = 0

    def __del__(self):
        """Stepper destructor to get all pins to low.
        """
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.LOW)
        GPIO.output(GPIO_TRIGGER_180, GPIO.LOW)
        GPIO.cleanup()

    def disconnect(self):
        """Stepper disconnect method to call destructor.
        """
        self.__del__()

    def move_at_angle_with_gpio_toggle(self, angle_in_degree=360, direction=False):
        """Method to perform the stepper motion and GPIO toggle.
        :param angle_in_degree: Angle to move stepper in degrees.
        :param direction: False-Clockwise, True-Anti-Clockwise.
        :return: Bool
        """
        try:
            GPIO.output(GPIO_TRIGGER_180, GPIO.LOW)
            i = 0
            step_count = int(angle_in_degree / degree_to_step)
            logger.info(f"Steps: {step_count}, angle: {angle_in_degree}")
            angle_in_degree = 0
            last_toggle_angle = 0
            for i in range(step_count):
                for pin in range(0, len(motor_pins)):
                    GPIO.output( motor_pins[pin], step_sequence[self.motor_step_counter][pin] )
                if direction:
                    self.motor_step_counter = (self.motor_step_counter - 1) % 8
                else:
                    self.motor_step_counter = (self.motor_step_counter + 1) % 8

                angle_in_degree = int((i+1) * degree_to_step)
                # If angle rotated is a multiple of 180; toggle GPIO
                if angle_in_degree != 0 and angle_in_degree % 180 == 0 and last_toggle_angle != angle_in_degree:
                    logger.info(f"Angle in degree {angle_in_degree}. Toggling GPIO")
                    GPIO.output(GPIO_TRIGGER_180, not GPIO.input(GPIO_TRIGGER_180))
                    last_toggle_angle = angle_in_degree
                time.sleep(step_sleep)
            return True
        except Exception as e:
            logger.error(f"Exception during Stepper control: {e}")
            print(f"Exception: {e}")
            return False


if __name__ == '__main__':
    stepper = Stepper()
    stepper.move_at_angle_with_gpio_toggle(angle_in_degree=720)
