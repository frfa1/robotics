import numpy as np
import random

def robot_drive(action):
    if action == "forward":
        return (50, 50)
    elif action == "backward":
        return (-50,-50)

    elif action == "left":
        return (-50,50)

    elif action == "right":
        return (50,-50)
    
def next_state_index(left_distance_theta, right_distance_theta):
    """ 
        Method to get the next state index based on theta robot
    """
    min_distance = 0.5 # Minimum distance to outer bound of the arena
    if left_distance_theta < min_distance: 
        if right_distance_theta < min_distance:
            state_index = 3
        else: 
            state_index = 1
    else:
        if right_distance_theta < min_distance:
            state_index = 2
        else:
            state_index = 0

    return state_index
    
def next_state(index_of_action):
    """
    Defines the next state based on an action
    """
    if index_of_action == 0:
        return 1
    elif index_of_action == 1:
        return 1
    elif index_of_action == 2:
        return 1
    elif index_of_action == 3:
        return 1
    elif index_of_action == 4:
        return 1
    elif index_of_action == 5:
        return 1
    else:  
        return -1
    
def init_state_and_actions():
    # Distances to wall (in cm)
    states = [
        "b_w", # Both white
        "l_b", # Left black
        "r_b", # Right black
        "b_b", # Both black
    ]
    state_size = len(states)

    # Possible movements
    actions = [
        "forward",
        "backward",
        "left",
        "right",
    ]
    action_size = len(actions)

    # Rewards - Based on each state
    rewards = [
        0,
        0,
        0,
        -100 # If both sensors see the line
    ]

    # Initialize q-table values to 0
    Q = np.zeros((state_size, action_size))

    # Illegal moves

    # All moves
    moves = []
    historic_states = []

    #state = 1 # Initialize state as s1 (the first state)
    state = "b_w"
    return states, actions, rewards, moves, historic_states, Q, state, state_size


### Old
def close_to_wall(states, actions, rewards, moves, historic_states, Q, state, state_size):
    # step_size = 0.2 # size between each step

    index_of_state = states.index(state) # Get index of state

    ## Takes action based on exploitation/exploration
    epsilon = 0.1 # Percentage of exploration
    if random.uniform(0, 1) < epsilon: # Exploration
        action = random.choice(actions) # Random action in the state
        print('RANDOM ACTION', action)
    else: # Exploitation
        index_of_action = Q[index_of_state].argmax() # Get the index of the action at the state with highest reward
        action = actions[index_of_action]
        print('BEST ACTION', action)

    # From action to index
    index_of_action = actions.index(action)

    # Illegal moves: Continue to next iteration
    # i.e. backwards on first position, or forward on last position
    # if (index_of_state == 0 and index_of_action == 1) or (index_of_state == state_size-1 and index_of_action == 0):
    #     return states, actions, rewards, moves, historic_states, Q, state, state_size, (0,0)

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
    close_to_wall(init_state_and_actions())
