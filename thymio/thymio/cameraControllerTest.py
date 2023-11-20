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
import numpy as np

class ThymioController:
    def __init__(self):

        def behaviorOA(prox_values):
            """
            Obstacle avoidance behavior function.
            Given the proximity sensor values, it determines the Thymio's motion.
            """

            # If an object is detected in front
            if prox_values[2] > 1500:
                return -100, -100
            # If an object is detected on the left
            elif prox_values[0] > 1000:
                return -100, 100
            # If an object is detected on the right
            elif prox_values[4] > 1000:
                return 100, -100
            # If no object is detected, move forward
            else:
                return 500, 500

        # Use the ClientAsync context manager to handle the connection to the Thymio robot.
        with ClientAsync() as client:

            async def prog():
                """
                Asynchronous function controlling the Thymio's behavior.
                """

                print('INSIDE PROG')
                # Lock the node representing the Thymio to ensure exclusive access.
                with await client.lock() as node:

                    print('INSIDE LOCK')

                    # Wait for the robot's proximity sensors to be ready.
                    await node.wait_for_variables({"prox.horizontal"})
                    
                    node.send_set_variables({"leds.top": [0, 0, 32]})

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

                        # this will be the left part
                        left_part = image[:, :third]

                        # this will be the middle part
                        middle_part = image[:, third:2 * third]

                        # this will be the right part
                        right_part = image[:, 2 * third:]

                        # Apply Gaussian Blur to the image
                        blurred_image = cv2.GaussianBlur(image, (15, 15), 0)
                        cv2.imwrite('left_image.jpg', left_part)
                        cv2.imwrite('middle_image.jpg', middle_part)
                        cv2.imwrite('right_image.jpg', right_part)


                        # Convert the frame to HSV color space
                        hsv = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2HSV)

                        lower_color = np.array([0, 0, 0]) ## change the colours to your preferences
                        upper_color = np.array([40, 40, 40])

                        # Create a mask to threshold the frame
                        mask = cv2.inRange(hsv, lower_color, upper_color)

                        # Find contours in the mask
                        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                        # Check if any detected contour meets the size criteria
                        for contour in contours:
                            # contourArea calculates the approximate size of the found contour
                            area = cv2.contourArea(contour)

                            print(area)
                            if area > 500:
                                print(area)
                                # node.v.motor.right.target = 100
                                # node.v.motor.left.target = 100
                            else:
                                node.v.motor.right.target = 0
                                node.v.motor.left.target = 0

                        # Display the camera feed with detection results
                        cv2.waitKey(1)
                        node.flush()
                    # Release the camera and close the OpenCV window

                        await client.sleep(1)  # Pause for 0.3 seconds before the next iteration

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
