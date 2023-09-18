#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait

# Create your objects here.
ev3 = EV3Brick()

# Initialize motors
left_motor = Motor(Port.D)
right_motor = Motor(Port.A)

# Initialize sensors
left_sensor = ColorSensor(Port.S1)
right_sensor = ColorSensor(Port.S4)
middle_sensor = ColorSensor(Port.S3)

route = ["u", "l", "u", "r", "d", "l", "d", "r"]

# Initialize drive base
robot = DriveBase(left_motor, right_motor, wheel_diameter=826, axle_track=1700)

BLACK = 5
GRAY = 70

MIDDLE_SENSOR_WHITE = 70
MIDDLE_SENSOR_BLACK = 5
MIDDLE_SENSOR_THRESHOLD = (MIDDLE_SENSOR_WHITE + MIDDLE_SENSOR_BLACK) / 2
PROPORTIONAL_GAIN = 1.1

threshold = (BLACK + GRAY) / 2  # 32.5
DRIVE_SPEED = 200
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

def drive_forward(speed):
    should_drive = True
    while should_drive:
        deviation = middle_sensor.reflection() - MIDDLE_SENSOR_THRESHOLD
        turn_rate = PROPORTIONAL_GAIN * deviation
        robot.drive(speed, turn_rate)

        left_reflection = left_sensor.reflection()
        right_reflection = right_sensor.reflection()
        middle_reflection = middle_sensor.reflection()

        if (left_reflection < threshold) and (middle_reflection < threshold) and (right_reflection < threshold):
            should_drive = False
        elif middle_reflection < threshold and left_reflection < threshold:
            should_drive = False
        elif middle_reflection < threshold and right_reflection < threshold:
            should_drive = False

        wait(100)

def turn_and_drive(turn):
        robot.turn(turn)
        drive_forward(DRIVE_SPEED)

def push_diamond():
    drive_forward(DRIVE_SPEED)
    drive_forward(-DRIVE_SPEED)


def drive_direction(sign, previousSign):
    if sign == UP and previousSign == RIGHT:
        robot.straight(1000)
        turn_and_drive(LEFT_TURN)
    elif sign == UP and previousSign == LEFT:
        turn_and_drive(RIGHT_TURN)
    elif sign == UP and previousSign == DOWN:
        turn_and_drive(TURN_180)
    elif sign == LEFT and previousSign == UP:
        turn_and_drive(LEFT_TURN)
    elif sign == LEFT and previousSign == DOWN:
        robot.straight(1000)
        turn_and_drive(RIGHT_TURN)
    elif sign == LEFT and previousSign == RIGHT:
        turn_and_drive(TURN_180)
    elif sign == DOWN and previousSign == LEFT:
        robot.straight(1000)
        turn_and_drive(LEFT_TURN)
    elif sign == DOWN and previousSign == RIGHT:
        turn_and_drive(RIGHT_TURN)
    elif sign == DOWN and previousSign == UP:
        turn_and_drive(TURN_180)
    elif sign == RIGHT and previousSign == UP:
        turn_and_drive(RIGHT_TURN)
    elif sign == RIGHT and previousSign == DOWN:
        turn_and_drive(LEFT_TURN)
    elif sign == RIGHT and previousSign == LEFT:
        turn_and_drive(TURN_180)

for i, signs in enumerate(route):
    if i is not 0:
        sign = signs[0]
        previousSign = route[i - 1]
        if sign == route[i - 1]:
            drive_forward(DRIVE_SPEED)
            print(1)
        elif signs.__contains__('p'):
            drive_direction(sign, previousSign)
            push_diamond()
        else:
            drive_direction(sign, previousSign)
    else:
        if sign == UP:
            drive_forward()
        elif sign == RIGHT:
            turn_and_drive(RIGHT_TURN)
        elif sign == LEFT:
            turn_and_drive(LEFT_TURN)
        elif sign == DOWN:
            turn_and_drive(TURN_180)