#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()


# Write your program here.
#ev3.speaker.beep()

# Initialize a motor at port A & D
left_motor = Motor(Port.D)
right_motor = Motor(Port.A)

# Initialize sensors
left_sensor = ColorSensor(Port.S1)
right_sensor = ColorSensor(Port.S4)
middle_sensor = ColorSensor(Port.S3)

# Initialize drive base
robot = DriveBase(left_motor, right_motor, wheel_diameter=442, axle_track=1600)

BLACK = 5
GRAY = 80
threshold = (BLACK + GRAY) / 2 # 42.5

DRIVE_SPEED = 1000

PROPORTIONAL_GAIN = 1.2

while True:
    #right_deviation = right_sensor.reflection() - threshold # Black: 5 - 42.5 = ~-37  |  Gray: 80 - 42.5 = 37.5
    #left_deviation = left_sensor.reflection() - threshold
    #middle_deviation = middle_sensor.reflection() - threshold

    #if middle_deviation < threshold and right_deviation < threshold

    print(middle_sensor.reflection())
    print(threshold)
    print("")

    deviation = middle_sensor.reflection() - threshold
    turn_rate = PROPORTIONAL_GAIN * deviation

    # GO STRAIGHT
    if middle_sensor.reflection() < threshold:
        robot.drive(-DRIVE_SPEED, 0)
        if left_sensor.reflection() < threshold:
            robot.turn(5)
        if right_sensor.reflection() < threshold:
            robot.turn(-5)

    # GO RIGHT
    elif right_sensor.reflection() < threshold:
        robot.turn(90)

    # GO LEFT
    elif left_sensor.reflection() < threshold:
        robot.turn(-90)
    else:
        robot.straight(-170)
        robot.stop()

    # Black line in middle, black in one side - turn side or continue front

    # Black line in middle, black in both sides - turn either or continue front

    # No black line in front, gray in either side - turn either side (with black line)


    #deviation = middle_sensor.reflection() - threshold
    #turn_rate = PROPORTIONAL_GAIN * deviation
    #robot.drive(DRIVE_SPEED, turn_rate)
    wait(10)


# Go forward and backwards for one meter
#robot.straight(10700)#, wait=True)
#robot.turn(90)#, wait=True)
#robot.straight(5000)#, wait=True)


#robot.straight(7000)
#robot.curve(radius=6100, angle=54)

#robot.straight(-1000)


# Play a sound.
#ev3.speaker.beep()
# Run the motor up to 500 degrees per second. To a target angle of 90 degrees.
#test_motor.run_target(1500, 360)
# Play another beep sound.
#ev3.speaker.beep(1000, 500)

