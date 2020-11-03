from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (
    Motor, ColorSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch
from pybricks.robotics import DriveBase
import time


class ColorSorter(object):
    # Initializing objects needed
    ev3 = EV3Brick()

    # Initializing and assigning sensors
    # TODO: Update this when final robot is built
    color_sensor = ColorSensor(Port.B)
    claw_motor = Motor(Port.C)
    arm_motor = Motor(Port.D)
    conveyor_motor = Motor(Port.S1)

    # Initializing misc. values
    claw_grip_speed = -100
    claw_angle = 60
    arm_speed = -100
    arm_angle = 75
    conveyor_speed = -100
    conveyor_angle = 195

    # Initial RGB tresholds
    red_treshold = 50
    green_treshold = 50
    blue_treshold = 50

    def wait_for_button_input(self):
        while True:
            if self.ev3.buttons.pressed():
                self.ev3.speaker.beep()
                wait(500)
                break
            continue

    # TODO: Update calibrate method
    def calibrate(self, calibration_time=2):
        """
        Reads RGB values from the color sensor in the given time, and sets their average as a treshold
        """
        if calibration_time < 2:
            print(
                "Error: calibration time must be minimum 2 seconds, setting to 2 (default)...")
            calibration_time = 2

        # Initializes all needed variables to calculate average
        red_value = green_value = blue_value = readings = 0

        # Uses StopWatch object to keep track of time
        start_time = time.time()

        # Reads in rgb values until calibration time is reached
        while time.time() - start_time < calibration_time:
            self.conveyor_motor.run(self.conveyor_speed)
            red, green, blue = self.color_sensor.rgb()
            red_value += red
            green_value += green
            blue_value += blue
            readings += 1
        self.conveyor_motor.stop()

        # Avoid divison by zero error
        if readings == 0:
            readings = 1

        # Updates tresholds based on average of readings
        self.red_treshold = red_value // readings + 10
        self.green_treshold = green_value // readings + 10
        self.blue_treshold = blue_value // readings + 10
        print("Calibrated")

    def run_conveyor(self):
        self.conveyor_motor.run_angle(self.conveyor_speed, self.conveyor_angle)

    # TODO: write grip open and grip close methods (or grip open/close method?)
    def grip(self):
        self.claw_motor.run_angle(self.claw_grip_speed, self.claw_angle, then=Stop.HOLD)
        self.claw_grip_speed *= -1

    def read_color(self):
        """
        Reads RGB-values from the RGB-sensor, and compares the values to find which color it is. Returns a string of the color name.
        """
        red, green, blue = self.color_sensor.rgb()
        print("R: {}, G: {}, B: {}".format(red, green, blue))
        if red > 25 and green < 15 and blue < 40:
            print("Red detected")
            return "red"
        elif 33 < red < 53 and 13 < green < 33 and 9 < blue < 29:
            print("Yellow detected")
            return "yellow"
        else:
            print("No color recognized")
            return "none"

    def arm_up(self):
        self.arm_motor.run_angle(self.arm_speed, self.arm_angle, then=Stop.HOLD)

    def arm_down(self):
        self.arm_motor.run_angle((self.arm_speed*-1), self.arm_angle, then=Stop.HOLD)