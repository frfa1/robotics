#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait
import random

# Create your objects here.
ev3 = EV3Brick()

# Initialize motors
left_motor = Motor(Port.D)
right_motor = Motor(Port.A)

# Initialize sensors
left_sensor = ColorSensor(Port.S1)
right_sensor = ColorSensor(Port.S4)
middle_sensor = ColorSensor(Port.S3)

route = ["u", "l"]

# Initialize drive base
robot = DriveBase(left_motor, right_motor, wheel_diameter=826, axle_track=1700)

BLACK = 5
GRAY = 60
MIDDLE_EDGE = 25
threshold = (BLACK + GRAY) / 2  # 32.5
DRIVE_SPEED = 500
RIGHT_TURN = -90
LEFT_TURN = 90
TURN_180 = 180
LEFT_DIRECTION = 'left'
RIGHT_DIRECTION = 'right'

RIGHT = 'r'
LEFT = 'l'
UP = 'u'
DOWN = 'd'
# Constants for correction behavior
CORRECTION_DURATION = 500  # Time in milliseconds
CORRECTION_SPEED = 300     # Speed for correction

robot.turn(90)
exit()

def correct_robot(direction):
        if direction == LEFT_DIRECTION:
            robot.turn(-20)
        elif direction == RIGHT_DIRECTION:
            robot.turn(20)
        robot.drive(CORRECTION_SPEED, 0)
        wait(CORRECTION_DURATION)

def drive_forward():
    should_drive = True
    while should_drive:
        robot.drive(DRIVE_SPEED, 0)

        left_reflection = left_sensor.reflection()
        right_reflection = right_sensor.reflection()
        middle_reflection = middle_sensor.reflection()

        if (left_reflection < threshold) and (middle_reflection < threshold) and (right_reflection < threshold):
            print(17)
            should_drive = False
        elif middle_reflection < threshold and left_reflection < threshold:
            print(18)
            should_drive = False
        elif middle_reflection < threshold and right_reflection < threshold:
            print(19)
            should_drive = False
        #elif left_reflection < threshold:
        #    correct_robot(LEFT_DIRECTION)
        #elif right_reflection < threshold:
        #    correct_robot(RIGHT_DIRECTION)

        wait(100)

def turn_and_drive(turn):
        robot.turn(turn)
        drive_forward()


for i, sign in enumerate(route):
    if i is not 0:
        if sign == route[i - 1]:
            drive_forward()
            print(1)
        else:
            if sign == UP and route[i - 1] == RIGHT:
                turn_and_drive(LEFT_TURN)
                print(2)
            elif sign == UP and route[i - 1] == LEFT:
                turn_and_drive(RIGHT_TURN)
                print(3)
            elif sign == UP and route[i - 1] == DOWN:
                turn_and_drive(TURN_180)
                print(4)
            elif sign == LEFT and route[i - 1] == UP:
                turn_and_drive(LEFT_TURN)
                print(5)
            elif sign == LEFT and route[i - 1] == DOWN:
                turn_and_drive(RIGHT_TURN)
                print(5)
            elif sign == LEFT and route[i - 1] == RIGHT:
                turn_and_drive(TURN_180)
                print(6)
            elif sign == DOWN and route[i - 1] == LEFT:
                turn_and_drive(LEFT_TURN)
                print(7)
            elif sign == DOWN and route[i - 1] == RIGHT:
                turn_and_drive(RIGHT_TURN)
                print(8)
            elif sign == DOWN and route[i - 1] == UP:
                turn_and_drive(TURN_180)
                print(9)
            elif sign == RIGHT and route[i - 1] == UP:
                turn_and_drive(RIGHT_TURN)
                print(10)
            elif sign == RIGHT and route[i - 1] == DOWN:
                turn_and_drive(LEFT_TURN)
                print(11)
            elif sign == RIGHT and route[i - 1] == LEFT:
                turn_and_drive(TURN_180)
                print(12)
    else:
        if sign == 'u':
            drive_forward()
            print(13)
        elif sign == 'r':
            turn_and_drive(RIGHT_TURN)
            print(14)
        elif sign == 'l':
            turn_and_drive(LEFT_TURN)
            print(15)
        elif sign == 'd':
            turn_and_drive(TURN_180)
            print(16)