from tdmclient import ClientAsync
import asyncio
import random
import math

## State Machine:

## State Exploration the robot continues exploration with random wheel velocities to move around randomly. This behavior can simulate the robot exploring its environment.

class ThymioController:
    def __init__(self):
        self.client = None
        self.running = True
        self.state = "exploration"  # Initial state

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

        # State machine logic
        if self.state == "exploration":
            if min_distance < 0.05:  # If any sensor reads within 5 cm
                left_wheel_vel = -100  # Move backward
                right_wheel_vel = -100
                self.state = "obstacle_avoidance"  # Transition to obstacle avoidance state
            else:
                # Randomly change direction every 10 seconds (100 * robot_timestep)
                if random.randint(1, 1000) == 1:
                    left_wheel_vel = random.randint(-100, 100)
                    right_wheel_vel = random.randint(-100, 100)
        elif self.state == "obstacle_avoidance":
            # place holder for implementing against obstacles (e.g., PID controller or any navigation algorithm)
            # Update left_wheel_vel and right_wheel_vel based on the obstacle avoidance algorithm
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
