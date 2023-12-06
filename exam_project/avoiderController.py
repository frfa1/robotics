from tdmclient import ClientAsync
import numpy as np

avoider_program = """
var send_interval = 200  # time in milliseconds
timer.period[0] = send_interval
call prox.comm.enable(1)
leds.top = [0, 0, 32]
leds.bottom.left = [0, 0, 32]
leds.bottom.right = [0, 0, 32]

timer.period[0] = send_interval

onevent timer0
    prox.comm.tx = 2
    
onevent prox.comm
    if prox.comm.rx == 1 then
        leds.top = [32, 0, 32]
        leds.bottom.left = [32, 0, 32]
        leds.bottom.right = [32, 0, 32]
    end
    
"""
class AvoiderController:
    def __init__(self):
        speed = 200
        actions = [
            "forward",
            #"big_forward",
            "backward",
            #"big_backward",
            "left",
            "right",
        ]
        states = [
            "b_w", # Both white
            "l_b", # Left black
            "r_b", # Right black
            "b_b", # Both black
        ]
        def act_on_action(action):
            if (action == "forward"):
                return speed, speed
            elif (action == "backward"):
                return -speed, -speed
            elif (action == "left"):
                return -speed, speed
            elif (action == "right"):
                return speed, -speed
            
        def is_on_edge(sensor):
            if (sensor < 100):
                return True
            else:
                return False
        def get_state_index(left_sensor, right_sensor):
            left_on_edge = is_on_edge(left_sensor)
            right_on_edge = is_on_edge(right_sensor)

            if (not left_on_edge and not right_on_edge):
                state = states[0]
            elif (left_on_edge and right_on_edge):
                state = states[3]
            elif (left_on_edge):
                state = states[1]
            elif (right_on_edge):
                state = states[2]
            
            return states.index(state)
            
        with ClientAsync() as client:
            async def prog():
                """
                Asynchronous function controlling the Thymio.
                """

                # Lock the node representing the Thymio to ensure exclusive access.
                with await client.lock() as node:
                    # Compile and send the program to the Thymio.
                    error = await node.compile(avoider_program)
                    if error is not None:
                        print(f"Compilation error: {error['error_msg']}")
                    else:
                        error = await node.run()
                        if error is not None:
                            print(f"Error {error['error_code']}")

                    # Wait for the robot's proximity sensors to be ready.
                    await node.wait_for_variables({"prox.horizontal"})
                    with open('Q_table.npy', 'rb') as f:
                        Q = np.load(f)
                    print(Q)

                    print("Thymio started successfully!")

                    while True:
                        ambiant_sensor_left = node.v.prox.ground.reflected[0]
                        ambiant_sensor_right = node.v.prox.ground.reflected[1]
                        # get the values of the proximity sensors
                        prox_values = node.v.prox.horizontal

                        """
                        Get the value of the message received from the other Thymio
                        the value is 0 if no message has been received and 
                        gets set to a new value when a message is received" 
                        """

                        message = node.v.prox.comm.rx

                        if sum(prox_values) > 20000:
                            break
                        
                        index_of_state = get_state_index(ambiant_sensor_left, ambiant_sensor_right)

                        index_of_action = Q[index_of_state].argmax()

                        print('INDEX OF STATE: ', index_of_state)

                        action = actions[index_of_action]

                        print('ACTION TAKEN', action)

                        node.v.motor.left.target, node.v.motor.right.target = act_on_action(action)

                        # print(f"Current state: {get_state(ambiant_sensor_left, ambiant_sensor_right)}")
                        node.flush()  # Send the set commands to the robot.

                        await client.sleep(0.3)  # Pause for 0.3 seconds before the next iteration.

                    # Once out of the loop, stop the robot and set the top LED to red.
                    print("Thymio stopped successfully!")
                    node.v.motor.left.target = 0
                    node.v.motor.right.target = 0
                    node.v.leds.top = [32, 0, 0]
                    node.flush()


            # Run the asynchronous function to control the Thymio.
            client.run_async_program(prog)



if __name__ == "__main__":
    # Instantiate the ThymioController class, which initializes and starts the robot's behavior.
    AvoiderController()