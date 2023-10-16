from tdmclient import ClientAsync
import random

import time
from breezyslam.algorithms import RMHC_SLAM
from breezyslam.sensors import RPLidarA1 as LaserModel
from rplidar import RPLidar as Lidar
from thymio_vehicle import ThymioVehicle
from visualize_thymio_file import visualizer
from multiprocessing import Pipe
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

        def avoidanceBehavior(prox_values):
            left_wheel_speed = 0
            right_wheel_speed = 0
            min_distance = sum(prox_values)

            if min_distance > 4000:  # If any sensor reads within 5 cm
                left_wheel_speed = -100  # Move backward
                right_wheel_speed = -100
            else:
            # Randomly change direction every 10 seconds (100 * robot_timestep)
                # if random.randint(1, 1000) == 1:
                left_wheel_speed = random.randint(0, 200)
                right_wheel_speed = random.randint(0, 200)
                # else:
            return left_wheel_speed, right_wheel_speed

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
                    previous_distances = None
                    previous_angles = None

                    next(self.iterator)
                    while True:
                        in_front = False
                        items = [item for item in next(self.iterator)]
                        distances = [item[2] for item in items]
                        angles = [item[1] for item in items]

                        prox_values = node.v.prox.horizontal
                        ambiant_sensors = node.v.prox.ground.ambiant

                        # Now you can sum or use these individual values
                        if sum(prox_values) > 20000:
                            break

                        if sum(ambiant_sensors) > 10:
                            print('FOUND MINE')
                            self.pose[0], self.pose[1], self.pose[2] = self.slam.getpos()
                            print('CURRENT POSITION', self.pose[0], self.pose[1], self.pose[2])
                            break

                        
                        for angle, distance in zip(angles, distances):
                            if 175 <= angle <= 185 and distance < 600:
                                node.v.motor.left.target = 100
                                node.v.motor.right.target = -100
                                in_front = True
                                print("In front")   

                        if not in_front:
                            speeds = avoidanceBehavior(prox_values)
                            node.v.motor.left.target = speeds[1]
                            node.v.motor.right.target = speeds[0]
                        node.flush()  # Send the set commands to the robot.

                        poses = self.thymio.computePoseChange(time.time(), node.v.motor.left.target,  node.v.motor.right.target)

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
                        self.publish()


                        await client.sleep(0.03)  # Pause for 0.3 seconds before the next iteration.

                    # Once out of the loop, stop the robot and set the top LED to red.
                    print("Thymio stopped successfully!")
                    node.v.motor.left.target = 0
                    node.v.motor.right.target = 0
                    node.v.leds.top = [32, 0, 0]
                    node.flush()

            # Run the asynchronous function to control the Thymio.
            client.run_async_program(prog)

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

if __name__ == "__main__":
    # Instantiate the ThymioController class, which initializes and starts the robot's behavior.
    try:
        thymio = ThymioVehicle(wheel_radius_mm, half_axl_length_mm, None)
        slam = RMHC_SLAM(LaserModel(), MAP_SIZE_PIXELS, MAP_SIZE_METERS)
        # lidar = LidarController(LIDAR_DEVICE, slam, thymio)
        lidar = LidarController(LIDAR_DEVICE, slam, thymio)
    except KeyboardInterrupt:
        Running = False
        # lidar.stop()
        # lidar.disconnect()