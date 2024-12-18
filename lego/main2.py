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

#route = ["u", "l", "u", "r", "d", "l", "d", "r"]
#route = ["u", "l"]
#route = ["up", "l"]#, "rp", "l"]
#route = ["r", "r", "d", "l", "d", "l", "l", "u", "rp", "rp", "l", "l", "d", "r", "r", "r", "up", "up"]
#route = ["up", "up"]
#route = ["up", "r"]
# route = ["d", "rp", "rp", "l", "l", "d", "rp", "l", "d", "rp", "rp", "up", "r", "up", "lp", "r", "d", "l", "l", "l", "u", "rp", "l", "u", "r", "r", "dp", "r", "d", "lp", "lp"]
route = ["d", "rp", "rp", "l", "l", "d", "d", "rp", "rp", "u", "lp", "r", "r", "up"]

# Initialize drive base
robot = DriveBase(left_motor, right_motor, wheel_diameter=826, axle_track=1700)

RIGHT_BLACK = 3
RIGHT_WHITE = 50
LEFT_BLACK = 5
LEFT_WHITE = 85

MIDDLE_SENSOR_WHITE = 85
MIDDLE_SENSOR_BLACK = 9
MIDDLE_SENSOR_THRESHOLD = (MIDDLE_SENSOR_WHITE + MIDDLE_SENSOR_BLACK) / 2
PROPORTIONAL_GAIN = 1.2

#threshold = (BLACK + WHITE) / 2  # 32.5
right_threshold = (RIGHT_BLACK + RIGHT_WHITE) / 2  
left_threshold = (LEFT_BLACK + LEFT_WHITE) / 2  
DRIVE_SPEED = 300
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

def is_opposite_way(sign, nextSign):
    if sign == 'r' and nextSign == 'l':
        return True
    elif sign == 'r' and nextSign == 'l':
        return True
    elif sign == 'u' and nextSign == 'd':
        return True
    elif sign == 'd' and nextSign == 'u':
        return True

def drive_forward(speed):
    should_drive = True
    while should_drive:
        deviation = middle_sensor.reflection() - MIDDLE_SENSOR_THRESHOLD
        turn_rate = PROPORTIONAL_GAIN * deviation
        if speed < 0:
            turn_rate = turn_rate * -1
        robot.drive(speed, turn_rate)

        left_reflection = left_sensor.reflection()
        right_reflection = right_sensor.reflection()
        middle_reflection = middle_sensor.reflection()

        print("left:", left_reflection)
        print("middle:", middle_reflection)
        print("right:", right_reflection)

        if (left_reflection < left_threshold) and (middle_reflection < MIDDLE_SENSOR_THRESHOLD) and (right_reflection < right_threshold):
            print(1)
            #exit()
            should_drive = False
        elif middle_reflection < MIDDLE_SENSOR_THRESHOLD and left_reflection < left_threshold:
            print(2)
            #exit()
            should_drive = False
        elif middle_reflection < MIDDLE_SENSOR_THRESHOLD and right_reflection < right_threshold:
            print(2)
            #exit()
            should_drive = False

        #wait(10)

def turn_and_drive(turn):
        if turn == 180:
            robot.turn(100)
            for i in range(0, 80, 1):
                middle_reflection = middle_sensor.reflection()
                if middle_reflection > MIDDLE_SENSOR_THRESHOLD:
                    robot.turn(1)
                else:
                    robot.turn(5)
        else:
            robot.turn(turn)
        drive_forward(DRIVE_SPEED)

def push_diamond(sign, nextSign):
    robot.straight(1000)
    drive_forward(DRIVE_SPEED)
    robot.straight(-1000)
    turn_and_drive(180)
    drive_forward(DRIVE_SPEED)
    if not is_opposite_way(sign, nextSign):
        robot.straight(2000)
        turn_and_drive(180)


def drive_direction(sign, previousSign, containsP, nextSign):

    correctionDistance = 1000
    if containsP:
        correctionDistance = -1000

    if sign == UP and previousSign == RIGHT:
        robot.straight(correctionDistance)
        turn_and_drive(LEFT_TURN)

    elif sign == UP and previousSign == LEFT:
        robot.straight(correctionDistance)
        turn_and_drive(RIGHT_TURN)

    elif sign == UP and previousSign == DOWN:
        robot.straight(correctionDistance)
        turn_and_drive(0)

    elif sign == LEFT and previousSign == UP:
        robot.straight(correctionDistance)
        turn_and_drive(LEFT_TURN)

    elif sign == LEFT and previousSign == DOWN:
        robot.straight(correctionDistance)
        turn_and_drive(RIGHT_TURN)

    elif sign == LEFT and previousSign == RIGHT:
        robot.straight(correctionDistance)
        turn_and_drive(0)

    elif sign == DOWN and previousSign == LEFT:
        robot.straight(correctionDistance)
        turn_and_drive(LEFT_TURN)

    elif sign == DOWN and previousSign == RIGHT:
        robot.straight(correctionDistance)
        turn_and_drive(RIGHT_TURN)

    elif sign == DOWN and previousSign == UP:
        robot.straight(correctionDistance)
        turn_and_drive(0)

    elif sign == RIGHT and previousSign == UP:
        robot.straight(correctionDistance)
        turn_and_drive(RIGHT_TURN)

    elif sign == RIGHT and previousSign == DOWN:
        robot.straight(correctionDistance)
        turn_and_drive(LEFT_TURN)
        
    elif sign == RIGHT and previousSign == LEFT:
        robot.straight(correctionDistance)
        turn_and_drive(0)

for i, signs in enumerate(route):
    sign = signs[0]
    previousSign = route[i - 1][0]
    if i+1 < len(route):
        nextSign = route[i + 1][0]
    if i is not 0:
        if sign == route[i - 1][0]:
            robot.straight(1000)
            drive_forward(DRIVE_SPEED)
            if "p" in signs:
                push_diamond(sign, nextSign)
        elif "p" in signs:
            drive_direction(sign, previousSign, False, nextSign)
            push_diamond(sign, nextSign)
        else:
            drive_direction(sign, previousSign, False, nextSign)
    else:
        if sign == UP:
            drive_forward(DRIVE_SPEED)
        elif sign == RIGHT:
            turn_and_drive(RIGHT_TURN)
        elif sign == LEFT:
            turn_and_drive(LEFT_TURN)
        elif sign == DOWN:
            turn_and_drive(TURN_180)
        if "p" in signs:
            push_diamond(sign, nextSign)