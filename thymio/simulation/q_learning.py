import numpy as np
import random

def robot_drive(action):
    if action == "forward":
        return (100,100)
    elif action == "backward":
        return (-100,-100)

def next_state(index_of_action):
    """
    Defines the next state based on an action
    """
    if index_of_action == 0:
        return 1
    else:
        return -1
    
def init_state_and_actions():
    # Distances to wall (in cm)
    states = [
        1, # (Or above)
        0.8,
        0.6,
        0.4,
        0.2,
        0,
    ]
    state_size = len(states)

    # Possible movements
    actions = [
        "forward", # Drives forward 20 cm
        "backward" # Drives backwards 20 cm
    ]
    action_size = len(actions)

    # Rewards - based on states indices (cm from wall)
    rewards = [
        0, # s1, 100 cm from wall
        0, # 80 cm from wall
        0, # 60 cm
        100, # 40 cm
        0, # 20 cm
        0 # 0 cm from wall
    ]

    # Initialize q-table values to 0
    Q = np.zeros((state_size, action_size))

    # Illegal moves
    Q[0,1] = -100
    Q[state_size-1, 0] = -100

    # All moves
    moves = []
    historic_states = []

    state = 1 # Initialize state as s1 (the first state)
    return states, actions, rewards, moves, historic_states, Q, state, state_size

def close_to_wall(states, actions, rewards, moves, historic_states, Q, state, state_size):
    # step_size = 0.2 # size between each step

    index_of_state = states.index(state) # Get index of state

    ## Takes action based on exploitation/exploration
    epsilon = 0.1 # Percentage of exploration
    if random.uniform(0, 1) < epsilon: # Exploration
        action = random.choice(actions) # Random action in the state
    else: # Exploitation
        index_of_action = Q[index_of_state].argmax() # Get the index of the action at the state with highest reward
        action = actions[index_of_action]

    # From action to index
    index_of_action = actions.index(action)

    # Illegal moves: Continue to next iteration
    # i.e. backwards on first position, or forward on last position
    if (index_of_state == 0 and index_of_action == 1) or (index_of_state == state_size-1 and index_of_action == 0):
        return

    ## Updating Q-values
    lr, gamma = 0.1, 0.9 # Hyperparameters

    # Get next state index
    index_of_next_state = index_of_state + next_state(index_of_action)

    # Get the reward
    reward = rewards[index_of_next_state]

    #print("> INDICES")
    #print(index_of_state, index_of_action, index_of_next_state)

    # Updates Q with the future step (action taken)
    Q[index_of_state, index_of_action] = Q[index_of_state, index_of_action] + lr * (reward + gamma * np.max(Q[index_of_next_state, :]) - Q[index_of_state, index_of_action])

    
    # robot drive until reaching destination
    # lower_bound = states[index_of_next_state] - (step_size/10)
    # higher_bound = states[index_of_next_state] + (step_size/10)
    # if not (lower_bound <= distance <= higher_bound): # Drive action until reaches goal state
    #     left_wheel_velocity, right_wheel_velocity = robot_drive(action) # Tuple of wheel velocities based on action
    # else: 
    #     doStuff = True
    # History of states and moves
    historic_states.append(state)
    moves.append(action)

    # Updates state before next iteration
    state = states[index_of_next_state]
    print(moves)
    print(historic_states)
    print(Q)

    return states, actions, rewards, moves, historic_states, Q, state, state_size, robot_drive(action)
    # return robot_drive(action)



if __name__ == "__main__":
    close_to_wall(init_state_and_actions(), True)
