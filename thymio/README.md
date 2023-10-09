# thymio

- username: pi

- Hostname: Robo

- kode: RoboRobo

# Connect to Rasberry Pi Server

- ssh pi@Robolocal

- Password : RoboRobo 

# Inside Rasberry Pi (terminal 1)

- flatpak run --command=thymio-device-manager org.mobsya.ThymioSuite

# Inside Rasberry Pi (terminal 2)

- cd ~/BreezySLAM/python/breezyslam

- python3.11 SLAM.py

# visualizer (terminal 3 )

- cd visualizer 
- python3.11 Visualizer.py
