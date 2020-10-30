from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (
    Motor, ColorSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch
from pybricks.robotics import DriveBase


class ColorSorter(object):
    """
    docstring
    """

    # Defining objects
    ev3 = EV3Brick()
    sw = StopWatch()

    # Defining sensors
    # TODO: Update this when final robot is built
    color_sensor = ColorSensor(Port.S1)
    claw_motor = Motor(Port.A)
    # self.arm_motor = Motor(Port.B)
    conveyor_motor = Motor(Port.C)

    # Defining default tresholds for color calibration
    red_treshold = 50
    green_treshold = 50
    blue_treshold = 50

    # Definings speeds
    claw_grip_speed = 100

    # Defining torque max
    claw_grip_duty_limit = 90 # min: 0, max: 100

    def __init__(self):
        """
        docstring
        """

    def calibrate(self, calibration_time=2):
        """
        Reads RGB values from the color sensor in the given time, and sets their average as a treshold
        """
        if calibration_time < 2:
            print("Error: calibration time must be minimum 2 seconds, setting to 2 (default)...")
            calibration_time = 2

        # Initializes all needed variables to calculate average
        red_value = green_value = blue_value = readings = 0

        # Uses StopWatch object to keep track of time
        start_time = self.sw.time()

        # Reads in rgb values until calibration time is reached
        while self.sw.time() - start_time < calibration_time:
            red, green, blue = self.color_sensor.rgb()
            red_value += red
            green_value += green
            blue_value += blue
            readings += 1

        # Avoid divison by zero error
        if readings == 0:
            readings = 1

        # Updates tresholds based on average of readings
        self.red_treshold = red_value // readings
        self.green_treshold = green_value // readings
        self.blue_treshold = blue_value // readings

    def is_black(self):
        red, green, blue = self.color_sensor.rgb()
        if red < red_treshold and green < green_treshold and blue < blue_treshold:
            return True
        else:
            return False

    def wait_for_button_input(self):
        """
        docstring
        """
        while True:
            if self.ev3.buttons.pressed():
                self.ev3.speaker.beep()
                wait(500)
                break
            continue

    def run_conveyor(self):
        """
        docstring
        """
        while True:
            self.conveyor_motor.run(-100)

    def grip(self):
        self.claw_motor.run_until_stalled(self.claw_grip_speed, then=Stop.HOLD, duty_limit=self.claw_grip_duty_limit)
        self.claw_grip_speed *= -1