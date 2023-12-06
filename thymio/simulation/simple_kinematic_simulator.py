import shapely
from shapely.geometry import LinearRing, LineString, Point
from numpy import sin, cos, pi, sqrt
import numpy as np
# from random import random
import random
import math

#import matplotlib.pyplot as plt
#import geopandas as gpd

from final_q_learning import close_to_wall, init_state_and_actions, next_state, robot_drive, next_state_index

# A prototype simulation of a differential-drive robot with one sensor

# Constants
###########
R = 0.0365  # radius of wheels in meters
L = 0.077

W = 40.0  # width of arena # Measured 190x110 cm
H = 40.0  # height of arena

thymio_size = 13.0 # width and height of thymio in cm (almost square)

DISTANCE_INTERVAL = 1

#robot_timestep = 0.1        # 1/robot_timestep equals update frequency of robot
robot_timestep = 0.05
simulation_timestep = 0.01  # timestep in kinematics sim (probably don't touch..)

# the world is a rectangular arena with width W and height H
world = LinearRing([(W/2,H/2),(-W/2,H/2),(-W/2,-H/2),(W/2,-H/2)])

print(list(world.coords))

# Variables 
###########

x = 0.0   # robot position in meters - x direction - positive to the right 
y = 0.0   # robot position in meters - y direction - positive up
q = 0.0   # robot heading with respect to x-axis in radians 

x_theta, y_theta, q_theta = 0.0, 0.0, 0.0 # Used for simulating next

left_wheel_velocity =  0   # robot left wheel velocity in radians/s
right_wheel_velocity =  0  # robot right wheel velocity in radians/s

left_wheel_velocity_theta, right_wheel_velocity_theta =  0, 0   # robot left and right wheel velocity in radians/s

sensor_radians = 2.5 * math.pi / 180 # Goes from 10 degrees to radians, to get left and right sensor angles

# Kinematic model
#################
# updates robot position and heading based on velocity of wheels and the elapsed time
# the equations are a forward kinematic model of a two-wheeled robot - don't worry just use it
def simulationstep():
    global x, y, q

    for step in range(int(robot_timestep/simulation_timestep)):     #step model time/timestep times
        v_x = cos(q)*(R*left_wheel_velocity/2 + R*right_wheel_velocity/2) 
        v_y = sin(q)*(R*left_wheel_velocity/2 + R*right_wheel_velocity/2)
        omega = (R*right_wheel_velocity - R*left_wheel_velocity)/(2*L)    
    
        x += v_x * simulation_timestep
        y += v_y * simulation_timestep
        q += omega * simulation_timestep

def simulationstep_theta():
    global x_theta, y_theta, q_theta

    for step in range(int(robot_timestep/simulation_timestep)):     #step model time/timestep times
        v_x = cos(q_theta)*(R*left_wheel_velocity_theta/2 + R*right_wheel_velocity_theta/2) 
        v_y = sin(q_theta)*(R*left_wheel_velocity_theta/2 + R*right_wheel_velocity_theta/2)
        omega = (R*right_wheel_velocity_theta - R*left_wheel_velocity_theta)/(2*L)    
    
        x_theta += v_x * simulation_timestep
        y_theta += v_y * simulation_timestep
        q_theta += omega * simulation_timestep

coordinates = []

# Simulation loop
#################
states, actions, rewards, moves, historic_states, Q, state, state_size = init_state_and_actions()
file = open("trajectory.dat", "w")
doStuff = True
for cnt in range(50000):

    # Reset robot every xth step
    """if cnt % 1000 == 0:
        x, y, q = 0.0, 0.0, 0.0
        #x, y, q = random.randint(-W//2, W//2), random.randint(-H//2, H//2), random.uniform(0, 2*math.pi)
        state = states[0]"""

    # Reset robot everytime the last 4 states are both sensors black
    """if cnt > 10:
        if historic_states[-1] == historic_states[-2] == historic_states[-3] == historic_states[-4] == historic_states[-5] == states[-1]:
            x, y, q = 0.0, 0.0, 0.0
            state = states[0]"""

    print("### ITERATION " + str(cnt) + " ###")
    print("ROBOT POSITION ", x, y, q)

    #simple single-ray sensor
    #ray = LineString([(x, y), (x+cos(q)*2*(W+H),(y+sin(q)*2*(W+H))) ])  # a line from robot to a point outside arena in direction of q
    """left_sensor = LineString([(x, y), (x+cos(q-sensor_radians)*2*(W+H),(y+sin(q-sensor_radians)*2*(W+H))) ])  # a line from robot to a point outside arena in direction of q
    right_sensor = LineString([(x, y), (x+cos(q+sensor_radians)*2*(W+H),(y+sin(q+sensor_radians)*2*(W+H))) ])  # a line from robot to a point outside arena in direction of q

    s = world.intersection(ray)
    distance = sqrt((s.x-x)**2+(s.y-y)**2) 

    left_s = world.intersection(left_sensor)
    left_distance = sqrt((left_s.x-x)**2+(left_s.y-y)**2)    
    right_s = world.intersection(right_sensor)
    right_distance = sqrt((right_s.x-x)**2+(right_s.y-y)**2)                     # distance to wall"""
    
    #simple controller - change direction of wheels every 10 seconds (100*robot_timestep) unless close to wall then turn on spot
    # if (distance < 0.5):
    #     left_wheel_velocity = -0.4
    #     right_wheel_velocity = 0.4
    # else:                
    #     if cnt%100==0:
    #         left_wheel_velocity = random()
    #         right_wheel_velocity = random()
    #print('DISTANCE: ', distance)
    if doStuff:
        print('doing stuff')
        index_of_state = states.index(state) # Get index of state

        ## Takes action based on exploitation/exploration
        epsilon = 0.2 # Percentage of exploration
        if random.uniform(0, 1) < epsilon: # Exploration
            action = random.choice(actions) # Random action in the state
            print('RANDOM ACTION', action)
        else: # Exploitation
            index_of_action = Q[index_of_state].argmax() # Get the index of the action at the state with highest reward
            action = actions[index_of_action]
            print('BEST ACTION', action)

        # From action to index
        index_of_action = actions.index(action)

        ### Run a theta simulation step to get the rewards of the next state
        x_theta, y_theta, q_theta = x, y, q # Reset Theta values since last step
        left_wheel_velocity_theta, right_wheel_velocity_theta = robot_drive(action)
        simulationstep_theta() # Simulate to get next state based on action
        ### Simulate movements of theta robot

        ##ray = LineString([(x, y), (x+cos(q)*2*(W+H),(y+sin(q)*2*(W+H))) ])  # a line from robot to a point outside arena in direction of q
        ##left_sensor = LineString([(x, y), (x+cos(q-10)*2*(W+H),(y+sin(q-10)*2*(W+H))) ])
        ##s = world.intersection(ray)
        ##distance = sqrt((s.x-x)**2+(s.y-y)**2)

        print("THETA ROBOT POSITION ", x_theta, y_theta, q_theta)

        ## Updating Q-values
        lr, gamma = 0.1, 0.9 # Hyperparameters

        try:
            left_sensor_theta = LineString([(x_theta, y_theta), (x_theta+cos(q_theta-sensor_radians)*2*(W+H),(y_theta+sin(q_theta-sensor_radians)*2*(W+H))) ])  # a line from robot to a point outside arena in direction of q
            right_sensor_theta = LineString([(x_theta, y_theta), (x_theta+cos(q_theta+sensor_radians)*2*(W+H),(y_theta+sin(q_theta+sensor_radians)*2*(W+H))) ])  # a line from robot to a point outside arena in direction of q
            
            left_s_theta = world.intersection(left_sensor_theta)
            left_distance_theta = sqrt((left_s_theta.x-x_theta)**2+(left_s_theta.y-y_theta)**2)    
            right_s_theta = world.intersection(right_sensor_theta)
            right_distance_theta = sqrt((right_s_theta.x-x_theta)**2+(right_s_theta.y-y_theta)**2)  # distance to wall

            print("DISTANCES ", left_distance_theta, right_distance_theta)

            # Illegal moves: Continue to next iteration
            # i.e. backwards on first position, or forward on last position
            #if (index_of_state == 0 and index_of_action == 1) or (index_of_state == state_size-1 and index_of_action == 0):
            #    continue

            # Get next state index
            #index_of_next_state = index_of_state + next_state(index_of_action)
            index_of_next_state = next_state_index(left_distance_theta, right_distance_theta)
        
        except:
            x, y, q = 0.0, 0.0, 0.0
            state = states[0]
            continue
            #index_of_next_state = 3

        # Get the reward
        reward = rewards[index_of_next_state]

        # Updates Q with the future step (action taken)
        Q[index_of_state, index_of_action] = Q[index_of_state, index_of_action] + lr * (reward + gamma * np.max(Q[index_of_next_state, :]) - Q[index_of_state, index_of_action])

        #print("> INDICES")
        #print(index_of_state, index_of_action, index_of_next_state)

        
        historic_states.append(state)
        moves.append(action)
        coordinates.append((x,y))

        # Updates state before next iteration
        state = states[index_of_next_state]

        # states, actions, rewards, moves, historic_states, Q, state, state_size, speeds = close_to_wall(states, actions, rewards, moves, historic_states, Q, state, state_size)
    """step_size = 1 # size between each step
    lower_bound = states[states.index(state)] - (step_size/10)
    higher_bound = states[states.index(state)] + (step_size/10)
    if not (lower_bound <= distance <= higher_bound): # Drive action until reaches goal state
        print('NOT DOING STUFF')
        doStuff = False
        left_wheel_velocity, right_wheel_velocity = robot_drive(action) # Tuple of wheel velocities based on action
    else: 
        doStuff = True"""
    left_wheel_velocity, right_wheel_velocity = robot_drive(action)

    #step simulation
    simulationstep()

    #check collision with arena walls 
    #if (world.distance(Point(x,y))<L/2):
    #    print("Collision with arena walls. Simulation stopping.")
    #    break
    if cnt%50==0:
        print(f"Recording data at time step {cnt}:")
        print(f"x: {x}, y: {y}, cos(q): {cos(q) * 0.2}, sin(q): {sin(q) * 0.2}")
        file.write(str(x) + ", " + str(y) + ", " + str(cos(q) * 0.2) + ", " + str(sin(q) * 0.2) + "\n")


f = open("simulation_output.txt", "a")
f.write("--- MOVES ---")
#f.write(moves)
f.write("--- HISTORIC STATES ---")
#f.write(historic_states)
f.write("--- COORDINATES ---")
#f.write(coordinates)
f.write("--- Q ---")
#f.write(Q)
f.close()

print(Q)

#print(moves)
#print(historic_states)
#print(coordinates)
#print(Q)

file.close()