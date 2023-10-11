from rplidar import RPLidar

LIDAR_DEVICE = '/dev/ttyUSB0'

lidar = RPLidar(LIDAR_DEVICE)

info = lidar.get_info()
print(info)

health = lidar.get_health()
print(health)

for i, scan in enumerate(lidar.iter_scans()):
    print('%d: Got %d measurments' % (i, len(scan)))
    if i > 10:
        break

lidar.stop()
lidar.stop_motor()
lidar.disconnect()