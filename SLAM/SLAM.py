import time
from breezyslam.algorithms import RMHC_SLAM
from breezyslam.sensors import RPLidarA1 as LaserModel
from rplidar import RPLidar as Lidar
from thymio_vehicle import ThymioVehicle
from visualize_thymio_file import visualizer
import asyncio
from multiprocessing import Pipe

MAP_SIZE_PIXELS = 250
MAP_SIZE_METERS = 15
LIDAR_DEVICE = '/dev/ttyUSB0'
wheel_radius_mm = 21
half_axl_length_mm = 45

class LidarController:
    def __init__(self, device, slam_obj, thymio_vehicle_obj, controller_pipe):
        self.lidar = Lidar(device)
        self.slam = slam_obj
        self.thymio = thymio_vehicle_obj
        self.viz = visualizer()
        self.pose = [0, 0, 0]
        self.controller_pipe = controller_pipe

        self.mapbytes = bytearray(MAP_SIZE_PIXELS * MAP_SIZE_PIXELS)
        self.MIN_SAMPLES = 50
        self.iterator = self.lidar.iter_scans()

    async def update(self):
        previous_distances = None
        previous_angles = None

        next(self.iterator)
        while True:

            items = [item for item in next(self.iterator)]
            distances = [item[2] for item in items]
            angles = [item[1] for item in items]

            left_speed = 0
            right_speed = 0

            poses = self.thymio.computePoseChange(time.time(), left_speed, right_speed)

            if len(distances) > self.MIN_SAMPLES:
                self.slam.update(distances, pose_change=poses, scan_angles_degrees=angles)
                previous_distances = distances.copy()
                previous_angles = angles.copy()
            elif previous_distances is not None:
                self.slam.update(previous_distances, scan_angles_degrees=previous_angles)

            self.pose[0], self.pose[1], self.pose[2] = self.slam.getpos()
            print(self.pose[0], self.pose[1], self.pose[2])

            self.slam.getmap(self.mapbytes)

            if self.controller_pipe.poll():
                message = self.controller_pipe.recv()
                if message == "FOUND SILVER ORE":
                    self.handle_silver_ore_detection()

            await asyncio.sleep(0.03)

    def handle_silver_ore_detection(self):
        print("SLAM Algorithm: Detected Silver Ore, Position:", self.pose)

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

async def mainLoop(lidar, delay):
    task = asyncio.create_task(lidar.update())
    while Running:
        lidar.publish()
        await asyncio.sleep(delay)
    lidar.stop()
    lidar.disconnect()
    await task

if __name__ == "__main__":
    try:
        thymio = ThymioVehicle(wheel_radius_mm, half_axl_length_mm, None)
        slam = RMHC_SLAM(LaserModel(), MAP_SIZE_PIXELS, MAP_SIZE_METERS)
        controller_pipe, slam_pipe = Pipe()
        lidar = LidarController(LIDAR_DEVICE, slam, thymio, controller_pipe)
        loop = asyncio.run(mainLoop(lidar, 0.5))
    except KeyboardInterrupt:
        Running = False
        lidar.stop()
        lidar.disconnect()
