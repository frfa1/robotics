from tdmclient import ClientAsync
import asyncio
import random
import math


# Controller (thymiocontroller.py):

# Controls a Thymio robot's behavior using the tdmclient library to connect to the robot.
# The robot uses proximity sensors to detect obstacles in its environment.
# Implements an obstacle avoidance behavior: if any proximity sensor detects an obstacle within 5 cm, the robot moves backward; otherwise, it may change direction randomly every 10 seconds or continue moving forward.
# The script is asynchronous and runs the controller logic in a loop, continuously updating the robot's behavior based on sensor inputs.


class ThymioController:
    def __init__(self):
        self.client = None
        self.running = True

    async def start(self):
        try:
            self.client = ClientAsync()
            async with self.client:
                await self.run_controller()
        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            self.stop()

    def stop(self):
        self.running = False
        if self.client is not None:
            self.client.close()

    async def obstacle_avoidance_behavior(self, prox_values):
        left_wheel_vel = 0
        right_wheel_vel = 0
        min_distance = min(prox_values)

        if min_distance < 0.05:  # If any sensor reads within 5 cm
            left_wheel_vel = -100  # Move backward
            right_wheel_vel = -100
        else:
            # Randomly change direction every 10 seconds (100 * robot_timestep)
            if random.randint(1, 1000) == 1:
                left_wheel_vel = random.randint(-100, 100)
                right_wheel_vel = random.randint(-100, 100)
            else:
                # Implement more advanced obstacle avoidance logic here
                pass

        return left_wheel_vel, right_wheel_vel

    async def run_controller(self):
        while self.running:
            try:
                async with self.client.lock() as node:
                    await node.wait_for_variables({"prox.horizontal"})
                    prox_values = node.v.prox.horizontal

                    if sum(prox_values) > 20000:
                        break

                    left_wheel_vel, right_wheel_vel = await self.obstacle_avoidance_behavior(prox_values)
                    node.v.motor.left.target = left_wheel_vel
                    node.v.motor.right.target = right_wheel_vel
                    node.flush()
            except Exception as e:
                print(f"Controller error: {str(e)}")

            # Pause for 0.3 seconds before the next iteration
            await asyncio.sleep(0.3)

        # Once out of the loop, stop the robot and set the top LED to red.
        print("Thymio stopped successfully!")
        node.v.motor.left.target = 0
        node.v.motor.right.target = 0
        node.v.leds.top = [32, 0, 0]
        node.flush()


if __name__ == "__main__":
    thymio_controller = ThymioController()
    asyncio.run(thymio_controller.start())
