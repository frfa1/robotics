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



#Test course code:

# # Constants for correction behavior
# CORRECTION_DURATION = 500  # Time in milliseconds
# CORRECTION_SPEED = 300     # Speed for correction

# while True:
#     # Read sensor values
#     left_reflection = left_sensor.reflection()
#     right_reflection = right_sensor.reflection()
#     middle_reflection = middle_sensor.reflection()

#     # Determine the state based on sensor readings
#     if left_reflection < threshold and middle_reflection < threshold and right_reflection < threshold:
#         state = "all_black"
#     elif middle_reflection < threshold and left_reflection < threshold:
#         state = "front_and_left"
#     elif middle_reflection < threshold and right_reflection < threshold:
#         state = "front_and_right"
#     elif left_reflection < threshold and right_reflection < threshold:
#         state = "left_and_right"
#     elif left_reflection < threshold:
#         state = "left"
#     elif right_reflection < threshold:
#         state = "right"
#     else:
#         state = "none_black"

#     # Print sensor values and current state
#     print("Left:", left_reflection)
#     print("Middle:", middle_reflection)
#     print("Right:", right_reflection)
#     print("State:", state)

#     # Correction behavior when no sensors are on black
#     if state == "none_black":
#         robot.drive(CORRECTION_SPEED, 0)
#         wait(CORRECTION_DURATION)
#         robot.stop()

#     # Make decisions based on the current state
#     else:
#         # Create a list of possible directions based on the current state
#         possible_directions = []

#         if "front" in state:
#             possible_directions.append("forward")
#         if "left" in state:
#             possible_directions.append("left")
#         if "right" in state:
#             possible_directions.append("right")

#         random_decision = random.choice(possible_directions)

#         if random_decision == "forward":
#             robot.drive(DRIVE_SPEED, 0)
#         elif random_decision == "left":
#             robot.turn(-90)
#         elif random_decision == "right":
#             robot.turn(90)

#     wait(100)

