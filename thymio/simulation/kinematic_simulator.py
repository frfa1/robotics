import shapely
from shapely.geometry import LinearRing, LineString, Point
from numpy import sin, cos, pi, sqrt
from random import random

## Simulator:

#Simulates the movement of a robot with kinematic constraints within a rectangular arena.
#The robot has simulated sensors (infrared sensors and bottom sensors) to detect its environment.
#The robot's position and orientation are updated based on its wheel velocities and elapsed time using a kinematic model.
#The script includes a simple controller that changes the direction of the robot's wheels randomly every 10 seconds, or it makes the robot turn on the spot if any sensor detects an obstacle within 5 cm.
#The simulation generates a trajectory data file ("trajectory.dat") that records the robot's position and orientation. 


# Constants
###########
R = 0.0365  # radius of wheels in meters
L = 0.077   # distance between wheels in meters

W = 2.0     # width of arena
H = 2.0     # height of arena

robot_timestep = 0.1        # 1/robot_timestep equals update frequency of robot
simulation_timestep = 0.01  # timestep in kinematics sim (probably don't touch..)

# the world is a rectangular arena with width W and height H
world = LinearRing([(W/2, H/2), (-W/2, H/2), (-W/2, -H/2), (W/2, -H/2)])

# Sensor Parameters
##################
sensor_positions = {
    1: (0.05, 0),    # Sensor 1 at 5 cm forward
    2: (-0.05, 0),   # Sensor 2 at 5 cm backward
    3: (0, 0.05),    # Sensor 3 at 5 cm to the right
    4: (0, -0.05),   # Sensor 4 at 5 cm to the left
    5: (0, 0),       # Sensor 5 at the robot's center
    6: (0, 0, -0.05), # Sensor 6 at 5 cm below
    7: (0, 0, 0.05),  # Sensor 7 at 5 below
}

# Maximum sensing range for the infrared sensors
front_and_back_sensors = {
    1: 4300,  # 1 cm
    2: 3500,  # 2 cm
    3: 2400,  # 3 cm
    4: 1600,  # 4 cm
    5: 0,     # 5 cm
}

# Bottom sensors data (provided)
bottom_sensors = {
    1: 300,  # 1 cm
    2: 130,  # 2 cm
}

# Variables
###########
x = 0.0   # robot position in meters - x direction - positive to the right
y = 0.0   # robot position in meters - y direction - positive up
q = 0.0   # robot heading with respect to x-axis in radians

left_wheel_velocity = random()   # robot left wheel velocity in radians/s
right_wheel_velocity = random()  # robot right wheel velocity in radians/s

# Kinematic model
#################
# updates robot position and heading based on velocity of wheels and the elapsed time
def simulationstep():
    global x, y, q

    for step in range(int(robot_timestep/simulation_timestep)):
        v_x = cos(q) * (R * left_wheel_velocity/2 + R * right_wheel_velocity/2)
        v_y = sin(q) * (R * left_wheel_velocity/2 + R * right_wheel_velocity/2)
        omega = (R * right_wheel_velocity - R * left_wheel_velocity) / (2 * L)

        x += v_x * simulation_timestep
        y += v_y * simulation_timestep
        q += omega * simulation_timestep

# Calculate Sensor Reading for One Sensor
#########################################
def calculate_sensor_reading(sensor_position, sensor_orientation):
    sensor_ray_endpoint = (x + cos(q + sensor_orientation) * sensor_position[0], y + sin(q + sensor_orientation) * sensor_position[0])
    sensor_ray = LineString([(x, y), sensor_ray_endpoint])
    intersection = world.intersection(sensor_ray)
    if intersection.is_empty:
        distance = front_and_back_sensors[5]  # Maximum range for Sensor 5 (center sensor)
    else:
        distance = sqrt((intersection.x - x)**2 + (intersection.y - y)**2)
    return distance

# Calculate Sensor Reading for Bottom Sensors
############################################
def calculate_bottom_sensor_reading(sensor_id):
    return bottom_sensors[sensor_id]

# Simulation loop
#################
file = open("trajectory.dat", "w")

for cnt in range(5000):
    # Update sensor readings
    sensor_readings = {}
    for sensor_id, sensor_position in sensor_positions.items():
        sensor_orientation = 0  # Adjust sensor orientation based on sensor_id if needed
        if sensor_id <= 4:
            reading = calculate_sensor_reading(sensor_position, sensor_orientation)
        else:
            reading = calculate_bottom_sensor_reading(sensor_id)
        sensor_readings[sensor_id] = reading

    # Simple controller - change direction of wheels every 10 seconds (100 * robot_timestep) unless close to wall, then turn on the spot
    if min(sensor_readings.values()) < 0.05:  # If any sensor reads within 5 cm
        left_wheel_velocity = -0.4
        right_wheel_velocity = 0.4
    else:
        if cnt % 100 == 0:
            left_wheel_velocity = random()
            right_wheel_velocity = random()

    # Step simulation
    simulationstep()

    # Check collision with arena walls
    if world.distance(Point(x, y)) < L/2:
        break

    if cnt % 50 == 0:
        file.write(str(x) + ", " + str(y) + ", " + str(cos(q) * 0.2) + ", " + str(sin(q) * 0.2) + "\n")

file.close()
