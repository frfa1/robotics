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

seeker_program = """
var send_interval = 200  # time in milliseconds
timer.period[0] = send_interval

leds.top = [32, 0, 0]
leds.bottom.left = [32, 0, 0]
leds.bottom.right = [32, 0, 0]

call prox.comm.enable(1)
onevent timer0
    prox.comm.tx = 1
"""

class SeekerController:
    def __init__(self):
        self.color_found = False

        def image_color(image):
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)    

            lower_color = np.array([189, 43, 67]) 
            upper_color = np.array([209, 83, 107])

            mask = cv2.inRange(hsv, lower_color, upper_color)

            return cv2.countNonZero(mask)

        with ClientAsync() as client:

            async def prog():
                with await client.lock() as node:
                    await node.wait_for_variables({"prox.horizontal"})
                    speed = 200
                    error = await node.compile(seeker_program)
                    if error is not None:
                        print(f"Compilation error: {error['error_msg']}")
                    else:
                        error = await node.run()
                        if error is not None:
                            print(f"Error {error['error_code']}")
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
                        
                        await client.sleep(0.15)

                        
                        message = node.v.prox.comm.rx
                        print(f"message from Thymio: {message}")

                        h, w, channels = image.shape

                        third = w // 3

                        left_part = image[:, :third]

                        middle_part = image[:, third:2 * third]

                        right_part = image[:, 2 * third:]

                        right_area = image_color(left_part)
                        middle_area = image_color(middle_part)
                        left_area = image_color(right_part)

                        print(right_area)
                                            
                        if middle_area > right_area and middle_area > left_area:
                            node.v.motor.right.target = speed
                            node.v.motor.left.target = speed
                        elif right_area > middle_area and right_area > left_area:
                            node.v.motor.right.target = speed
                            node.v.motor.left.target = -speed
                        elif left_area > middle_area and left_area > right_area:
                            node.v.motor.right.target = -speed
                            node.v.motor.left.target = speed
                        else:
                            node.v.motor.right.target = -speed
                            node.v.motor.left.target = speed
                        node.flush()
                        await client.sleep(0.15)


                    camera.release()
                    cv2.destroyAllWindows()
                    print("Thymio stopped successfully!")
                    node.v.motor.left.target = 0
                    node.v.motor.right.target = 0
                    node.flush()

            # Run the asynchronous function to control the Thymio.
            client.run_async_program(prog)


if __name__ == "__main__":
    # Instantiate the ThymioController class, which initializes and starts the robot's behavior.
    SeekerController()
