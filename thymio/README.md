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




# TEST THYMIO SPEED AND ANGLE

This is will run the thymio going straight for 10 seconds, and we will measure how far it drove and the off angle

tests with 100, 100 speed:
    1. 
        1. distance: 32.5 cm
        2. angles: front of robot: 1cm, back of robot: 0.4cm
    2.  
        1. distance: 33.1 cm
        2. angles: front of robot: 0cm, back of robot: 0cm
    3.
        1. distance: 33.2 cm
        2. angles: front of robot: 0cm, back of robot: 0cm
    4.
        1. distance: 33 cm
        2. angles: front of robot: 0.4cm, back of robot: 0.3cm
    5.
        1. distance: 33.2 cm
        2. angles: front of robot: 0cm, back of robot: 0cm


tests with 200, 200 speed:
    1. 
        1. distance: 64.3 cm
        2. angles: front of robot: -0.1cm, back of robot: -0.1cm
    2.  
        1. distance: 64.1 cm
        2. angles: front of robot: 0.6cm, back of robot: 0.5cm
    3.
        1. distance: 63.8 cm
        2. angles: front of robot: -1.2cm, back of robot: -0.8cm
    4.
        1. distance: 64.5 cm
        2. angles: front of robot: 1.4cm, back of robot: 0.9cm
    5.
        1. distance: 65.2 cm
        2. angles: front of robot: 0.5cm, back of robot: 0.4cm