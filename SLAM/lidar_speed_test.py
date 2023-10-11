from rplidar import RPLidar
import time

LIDAR_DEVICE = '/dev/ttyUSB0'

lidar = RPLidar(LIDAR_DEVICE)


t_end = time.time() + 60
while time.time() < t_end:
    print(len())

# for i, scan in enumerate(lidar.iter_scans()):
    
#     # anglesResult = " ".join(str(x) for x in angles)

#     zero_degrees = []
#     for item in scan:
#         angle = item[1]
#         if (angle < 1 or angle > 359):
#             zero_degrees.append(item)
#     print(zero_degrees)



#     # ninety_degrees = []
#     # for item in scan:
#     #     angle = item[1]
#     #     if (angle < 91 and angle > 89):
#     #         ninety_degrees.append(item)
#     # print('Ninety degrees, run: ', i, ninety_degrees)
#     # print('Angles: ' + anglesResult)

#     if i > 10:
#         break

lidar.stop()
lidar.stop_motor()
lidar.disconnect()