#!/usr/bin/env pybricks-micropython
from pybricks.tools import wait
from ColorSorter import ColorSorter


cs = ColorSorter()
# cs.grip()

while True:
    # cs.arm_up()
    # cs.grip()
    cs.wait_for_button_input()
    # color = cs.read_color()
    # cs.run_conveyor()
    # wait(500)
    # cs.arm_down()
    cs.grip()
    # cs.arm_up()
    # cs.sort(color)  # TODO: if color == "none": continue
