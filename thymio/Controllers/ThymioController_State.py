from tdmclient import ClientAsync
import asyncio
import random
import math

## State Machine:

## State Exploration the robot continues exploration with random wheel velocities to move around randomly. This behavior can simulate the robot exploring its environment.

class ThymioController:
    def __init__(self):

        def avoidanceBehavior(prox_values):
            left_wheel_vel = 0
            right_wheel_vel = 0
            min_distance = min(prox_values)

        # State machine logic
        if state == "exploration":
            if min < 0.05:  # If any sensor reads within 5 cm
                left_wheel_vel = -100  # Move backward
                right_wheel_vel = -100
                state = "obstacle_avoidance"  # Transition to obstacle avoidance state
            else:
                # Randomly change direction every 10 seconds (100 * robot_timestep)
                if random.randint(1, 1000) == 1:
                    left_wheel_vel = random.randint(-100, 100)
                    right_wheel_vel = random.randint(-100, 100)
                elif state == "obstacle_avoidance":
                    return left_wheel_vel, right_wheel_vel
                
with ClientAsync() as client:

    async def prog():

         with await client.lock() as node:

            await node.wait_for_variables({"prox.horizontal"})
            node.send_set_variables({"leds.top": [0, 0, 32]})
            print("Thymio started successfully!")
            while True:
                prox_values = node.v.prox.horizontal

                if sum(prox_values) > 20000:
                    break

                    speeds = avoidanceBehavior(prox_values)
                    node.v.motor.left.target = speeds[1]
                    node.v.motor.right.target = speeds[0]
                    node.flush()  # Send the set commands to the robot.

                await asyncio.sleep(0.3)  # Pause for 0.3 seconds before the next iteration

        # Once out of the loop, stop the robot and set the top LED to red.
                print("Thymio stopped successfully!")
                node.v.motor.left.target = 0
                node.v.motor.right.target = 0
                node.v.leds.top = [32, 0, 0]
                node.flush()

if __name__ == "__main__":
    thymio_controller = ThymioController()
    asyncio.run(thymio_controller.start())
