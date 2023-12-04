"""
Thymio Obstacle Avoidance Controller

This project utilizes the tdmclient library to control a Thymio robot. Specifically,
it makes use of the asynchronous client provided by the library to handle real-time reactions and non-blocking behaviors of the robot.

Important:
- The tdmclient library offers multiple ways of interacting with Thymio robots, both synchronously and asynchronously.
- The library provides capabilities to execute code both on the Thymio robot itself and on external platforms like a Raspberry Pi.
- This current implementation is based on polling the sensors continuously.
    However, for more advanced use-cases, users might want to design the code to be event-driven, reacting to specific triggers or states,
     which can offer more efficient and responsive behaviors.

Setup:
1. Ensure the Thymio robot is connected and powered on.
2. Ensure all required dependencies, including the tdmclient library, are installed.
3. Before running this script, make sure to start the Thymio device manager by executing the following command in the terminal:
    flatpak run --command=thymio-device-manager org.mobsya.ThymioSuite
4. Once the device manager is running, execute this script to initiate the obstacle avoidance behavior of the Thymio robot.
"""

from tdmclient import ClientAsync
import cv2
import itertools 
import numpy as np

class ThymioController:
    def __init__(self):
        self.color_found = False

        def image_color(image):
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)    

            lower_color = np.array([180, 35, 30]) 
            upper_color = np.array([250, 80, 110])

            mask = cv2.inRange(hsv, lower_color, upper_color)

            color_image = cv2.bitwise_and(image, image, mask=mask)
            return color_image

        with ClientAsync() as client:

            async def prog():
                with await client.lock() as node:
                    await node.wait_for_variables({"prox.horizontal"})
                    node.send_set_variables({"leds.top": [0, 0, 32]})
                    node.send_set_variables({"leds.bottom.left": [0, 0, 32]})
                    node.send_set_variables({"leds.bottom.right": [0, 0, 32]})

                    camera = cv2.VideoCapture(0)
                    cv2.startWindowThread()
                    print("Thymio started successfully!")
                    while True:
                        prox_values = node.v.prox.horizontal

                        if sum(prox_values) > 20000:
                            break

                        ret, image = camera.read()
                        if not ret:
                            break

                        h, w, channels = image.shape

                        third = w // 3

                        left_part = image[:, :third]

                        middle_part = image[:, third:2 * third]

                        right_part = image[:, 2 * third:]

                        left_area = image_color(left_part)
                        middle_area = image_color(middle_part)
                        right_area = image_color(right_part)

                        print(left_area)
                                            
                        if middle_area > left_area and middle_area > right_area:
                            node.v.motor.right.target = 100
                            node.v.motor.left.target = 100
                        elif left_area > middle_area and left_area > right_area:
                            node.v.motor.right.target = 100
                            node.v.motor.left.target = -100
                        elif right_area > middle_area and right_area > left_area:
                            node.v.motor.right.target = -100
                            node.v.motor.left.target = 100
                        else:
                            node.v.motor.right.target = 0
                            node.v.motor.left.target = 0
                        # left_contours, _ = image_color(left_part)
                        # middle_contours, _ = image_color(middle_part)
                        # right_contours, _ = image_color(right_part)


                        # for (left, middle, right) in zip(left_contours, middle_contours, right_contours):
                        #     left_area = cv2.contourArea(left)
                        #     middle_area = cv2.contourArea(middle)
                        #     right_area = cv2.contourArea(right)

                        #     print(left_area + middle_area + right_area)
                        #     if left_area + middle_area + right_area > 100:
                        #         node.v.motor.right.target = 0
                        #         node.v.motor.left.target = 0
                        #         color_found = True
                        #     else:
                        #         node.v.motor.right.target = 100
                        #         node.v.motor.left.target = -100
                        #         color_found = False
                        #     cv2.waitKey(1)

                        #     if color_found:
                        #         if middle_area > left_area and middle_area > right_area:
                        #             node.v.motor.right.target = 100
                        #             node.v.motor.left.target = 100
                        #         elif left_area > middle_area and left_area > right_area:
                        #             node.v.motor.right.target = 100
                        #             node.v.motor.left.target = -100
                        #         else:
                        #             node.v.motor.right.target = -100
                        #             node.v.motor.left.target = 100

                        #     elif not color_found:
                        #         node.v.motor.right.target = 0
                        #         node.v.motor.left.target = 0
                        node.flush()
                        await client.sleep(0.3)


                # Once out of the loop, stop the robot and set the top LED to red
                    camera.release()
                    cv2.destroyAllWindows()
                    print("Thymio stopped successfully!")
                    node.v.motor.left.target = 0
                    node.v.motor.right.target = 0
                    node.v.leds.top = [0, 0, 32]
                    node.flush()

            # Run the asynchronous function to control the Thymio.
            client.run_async_program(prog)


if __name__ == "__main__":
    # Instantiate the ThymioController class, which initializes and starts the robot's behavior.
    ThymioController()
