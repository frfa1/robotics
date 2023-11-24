from tdmclient import ClientAsync
import random
from multiprocessing import Pipe

class RoombaController:
    def __init__(self, slam_pipe):
        self.slam_pipe = slam_pipe

        with ClientAsync() as client:

            async def roomba_behavior():
                with await client.lock() as node:
                    await node.wait_for_variables({"prox.horizontal", "ground.ambiant", "leds.top"})

                    initial_ground_color = node.v.ground.ambiant[0]

                    print("Roomba started successfully!")

                    while True:
                        prox_values = node.v.prox.horizontal
                        current_ground_color = node.v.ground.ambiant[0]

                        if prox_values[2] > 1500:
                            if random.random() < 0.5:
                                self.turn_right(node)
                            else:
                                self.turn_left(node)
                        else:
                            self.move_forward(node)

                        # Check if silver ore is detected
                        if self.is_silver_ore_detected(initial_ground_color, current_ground_color):
                            self.change_behavior(node)

                        await client.sleep(0.3)

            client.run_async_program(roomba_behavior)

    def move_forward(self, node):
        node.v.motor.left.target = 100
        node.v.motor.right.target = 100
        node.flush()

    def turn_left(self, node):
        node.v.motor.left.target = -100
        node.v.motor.right.target = 100
        node.flush()

    def turn_right(self, node):
        node.v.motor.left.target = 100
        node.v.motor.right.target = -100
        node.flush()

    def stop_robot(self, node):
        node.v.motor.left.target = 0
        node.v.motor.right.target = 0
        node.flush()

    def is_silver_ore_detected(self, initial_ground_color, current_ground_color):
        threshold = 100 
        return abs(current_ground_color - initial_ground_color) > threshold

    def change_behavior(self, node):
        print("FOUND SILVER ORE, Roomba stopped successfully!")
        self.slam_pipe.send("FOUND SILVER ORE")

        self.stop_robot(node)
        node.v.leds.top = [0, 32, 0]
        node.flush()

if __name__ == "__main__":
    controller_pipe, slam_pipe = Pipe() 
    RoombaController(slam_pipe)
