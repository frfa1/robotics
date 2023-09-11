#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
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

# Initialize drive base
robot = DriveBase(left_motor, right_motor, wheel_diameter=442, axle_track=1600)

BLACK = 5
GRAY = 80
threshold = (BLACK + GRAY) / 2  # 42.5
DRIVE_SPEED = 1000

# Constants for correction behavior
CORRECTION_DURATION = 500  # Time in milliseconds
CORRECTION_SPEED = 300     # Speed for correction

while True:
    # Read sensor values
    left_reflection = left_sensor.reflection()
    right_reflection = right_sensor.reflection()
    middle_reflection = middle_sensor.reflection()

    # Determine the state based on sensor readings
    if left_reflection < threshold and middle_reflection < threshold and right_reflection < threshold:
        state = "front_and_left_and_right"
    elif middle_reflection < threshold and left_reflection < threshold:
        state = "front_and_left"
    elif middle_reflection < threshold and right_reflection < threshold:
        state = "front_and_right"
    elif left_reflection < threshold and right_reflection < threshold:
        state = "left_and_right"
    elif left_reflection < threshold:
        state = "left"
    elif right_reflection < threshold:
        state = "right"
    elif middle_reflection < threshold:
        state = "front"
    else:
        state = "none_black"

    # Print sensor values and current state
    print("Left:", left_reflection)
    print("Middle:", middle_reflection)
    print("Right:", right_reflection)
    print("State:", state)

    # Correction behavior when no sensors are on black
    if state == "none_black":
        robot.drive(CORRECTION_SPEED, 0)
        wait(CORRECTION_DURATION)
        robot.stop()

    # Make decisions based on the current state
    else:
        # Create a list of possible directions based on the current state
        possible_directions = []
        if "front" in state:
            possible_directions.append("front")
        if "left" in state:
            possible_directions.append("left")
        if "right" in state:
            possible_directions.append("right")

        random_decision = random.choice(possible_directions)

        if random_decision == "forward":
            robot.drive(DRIVE_SPEED, 0)
        elif random_decision == "left":
            robot.turn(-90)
        elif random_decision == "right":
            robot.turn(90)

    wait(100)
