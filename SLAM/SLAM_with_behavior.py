import time
from breezyslam.algorithms import RMHC_SLAM
from breezyslam.sensors import RPLidarA1 as LaserModel
from rplidar import RPLidar as Lidar
from thymio_vehicle import ThymioVehicle
from visualize_thymio_file import visualizer
import multiprocessing
from multiprocessing import Pipe
import asyncio
import json

MAP_SIZE_PIXELS = 250
MAP_SIZE_METERS = 15
LIDAR_DEVICE = '/dev/ttyUSB0'
wheel_radius_mm = 21
half_axl_length_mm = 45


class LidarController:
    def __init__(self, device, slam_obj, thymio_vehicle_obj):
        self.lidar = Lidar(device)
        self.slam = slam_obj
        self.thymio = thymio_vehicle_obj
        self.viz = visualizer()
        self.pose = [0, 0, 0]

        # Create an RMHC SLAM object with a laser model and optional robot model
        self.mapbytes = bytearray(MAP_SIZE_PIXELS * MAP_SIZE_PIXELS)
        self.MIN_SAMPLES = 50

        # Create an iterator to collect scan data from the RPLidar
        self.iterator = self.lidar.iter_scans()

    async def update(self):
        previous_distances = None
        previous_angles = None

        next(self.iterator)
        while True:  # Keep this infinite for demonstration

            # Extract (quality, angle, distance) triples from current scan
            items = [item for item in next(self.iterator)]
            distances = [item[2] for item in items]
            angles = [item[1] for item in items]

            # todo mack function that gets the speed from the thymio ( left_speed, left_speed)
            left_speed = 0
            right_speed = 0

            poses = self.thymio.computePoseChange(time.time(), left_speed, right_speed)

            # Update SLAM with current Lidar scan and scan angles if adequate
            if len(distances) > self.MIN_SAMPLES:
                self.slam.update(distances, pose_change=poses, scan_angles_degrees=angles)
                previous_distances = distances.copy()
                previous_angles = angles.copy()
            elif previous_distances is not None:
                self.slam.update(previous_distances, scan_angles_degrees=previous_angles)
            # Get current robot position
            self.pose[0], self.pose[1], self.pose[2] = self.slam.getpos()
            print(self.pose[0], self.pose[1], self.pose[2])

            # Get current map bytes as grayscale
            self.slam.getmap(self.mapbytes)

            await asyncio.sleep(0.03)

    def publish(self):

        self.viz.publish(self.mapbytes)
        self.viz.publish(
            json.dumps({"x_coord": str(self.pose[0]), "y_coord": str(self.pose[1]), "orientation": str(self.pose[2])}))

    def get_info(self):
        return self.lidar.get_info()

    def get_health(self):
        return self.lidar.get_health()

    def stop(self):
        self.lidar.stop()

    def disconnect(self):
        self.lidar.disconnect()


Running = True


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


class ThymioController:
    async def update(self):

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
                return 100, 100

        # Use the ClientAsync context manager to handle the connection to the Thymio robot.
        with ClientAsync() as client:

            async def prog():
                """
                Asynchronous function controlling the Thymio's behavior.
                """

                # Lock the node representing the Thymio to ensure exclusive access.
                with await client.lock() as node:

                    # Wait for the robot's proximity sensors to be ready.
                    await node.wait_for_variables({"prox.horizontal"})

                    node.send_set_variables({"leds.top": [0, 0, 32]})
                    print("Thymio started successfully!")
                    while True:
                        prox_values = node.v.prox.horizontal

                        if sum(prox_values) > 20000:
                            break

                        speeds = behaviorOA(prox_values)
                        node.v.motor.left.target = speeds[1]
                        node.v.motor.right.target = speeds[0]
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
    ThymioController()


async def mainLoop(lidar, delay, behavior):
    # task = asyncio.create_task(lidar.update())
    # task = asyncio.create_task(behavior.update())
    while Running:
        await asyncio.gather(lidar.update(), behavior.update())
        lidar.publish()
        await asyncio.sleep(delay)
    lidar.stop()
    lidar.disconnect()

if __name__ == "__main__":
    try:
        thymio = ThymioVehicle(wheel_radius_mm, half_axl_length_mm, None)
        slam = RMHC_SLAM(LaserModel(), MAP_SIZE_PIXELS, MAP_SIZE_METERS)
        lidar = LidarController(LIDAR_DEVICE, slam, thymio)
        behavior = ThymioController()
        loop = asyncio.run(mainLoop(lidar, 0.5, behavior))
    except KeyboardInterrupt:
        Running = False
        lidar.stop()
        lidar.disconnect()
