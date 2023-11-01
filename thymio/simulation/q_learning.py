import numpy as np
import random

def robot_drive(action):
    if "forward":
        return (100,100)
    elif "backward":
        return (-100,-100)

def next_state(index_of_action):
    """
    Defines the next state based on an action
    """
    if index_of_action == 0:
        return 1
    else:
        return -1

def close_to_wall():
    """
    Initial example of Q-learning where the robot is pointed towards a wall
    and learns to stay at a certain distance to the wall.
    """

    # Distances to wall (in cm)
    states = [
        100, # (Or above)
        80,
        60,
        40,
        20,
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

    state = 100 # Initialize state as s1 (the first state)
    for i in range(1000): # Number of simulation actions

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
            continue

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
        # while distance != states[index_of_next_state]: # Drive action until reaches goal state
        #   wheels = robot.drive(action) # Tuple of wheel velocities based on action

        # History of states and moves
        historic_states.append(state)
        moves.append(action)

        # Updates state before next iteration
        state = states[index_of_next_state]

    print(moves)
    print(historic_states)
    print(Q)


if __name__ == "__main__":
    close_to_wall()
