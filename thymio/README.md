# thymio

- username: pi

- Hostname: Robo

- kode: RoboRobo

# Connect to Rasberry Pi Server

- ssh pi@Robolocal

- Password : RoboRobo 

# Inside Rasberry Pi (terminal 1)

flatpak run --command=thymio-device-manager org.mobsya.ThymioSuite

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




## LIDAR TESTS:


   # Test for how many times we hit an interval between the angles 12 times
    
        Results for angles between 359 and 1:

        Run:  0 []
        Run:  1 [(15, 0.25, 325.25)]
        Run:  2 [(15, 359.4375, 340.75), (15, 0.640625, 327.25)]
        Run:  3 [(15, 359.234375, 359.25)]
        Run:  4 [(15, 359.90625, 342.0)]
        Run:  5 []
        Run:  6 [(15, 359.765625, 340.75)]
        Run:  7 [(15, 0.109375, 343.0)]
        Run:  8 [(15, 359.203125, 361.25), (15, 0.796875, 329.0)]
        Run:  9 [(15, 359.125, 359.25), (15, 0.953125, 328.75)]
        Run:  10 [(15, 359.953125, 340.25)]
        Run:  11 [(15, 0.234375, 327.0)]



    # Test where 0, 90, 180, 270, and 360 are

        



    # Test lidar distances:

    # SUDO ZERO (10 cm):
    Zero degrees, run:  0 []
Zero degrees, run:  1 []
Zero degrees, run:  2 []
Zero degrees, run:  3 []
Zero degrees, run:  4 []
Zero degrees, run:  5 []
Zero degrees, run:  6 []
Zero degrees, run:  7 []
Zero degrees, run:  8 []
Zero degrees, run:  9 []
Zero degrees, run:  10 []
Zero degrees, run:  11 []

    # 20 cm
[(15, 359.5, 208.25), (15, 0.8125, 198.25)]
[(15, 359.703125, 198.0)]
[(15, 359.5625, 198.0)]
[(15, 359.0625, 198.0), (15, 0.875, 198.25)]
[(15, 359.359375, 198.0)]
[(15, 359.34375, 197.75), (15, 0.640625, 198.0)]
[(15, 359.390625, 197.75), (15, 0.703125, 198.0)]
[(15, 359.796875, 198.0)]
[(15, 0.234375, 198.0)]
[(15, 359.375, 197.75), (15, 0.671875, 197.75)]
 [(15, 0.078125, 197.5)]
 [(15, 359.5625, 197.5), (15, 0.875, 198.25)]


    # 40cm

[(15, 359.4375, 387.5), (15, 0.671875, 387.25)]
[(15, 359.390625, 389.5), (15, 0.828125, 386.75)]
[(15, 359.125, 387.5), (15, 0.6875, 386.5)]
[(15, 359.671875, 387.25)]
[(15, 359.03125, 386.5), (15, 0.3125, 387.0)]
[(15, 0.6875, 386.5)]
[(15, 359.6875, 387.0)]
[(15, 0.03125, 386.75)]
[(15, 359.59375, 386.5)]
[(15, 359.015625, 386.25), (15, 0.75, 386.25)]
[(15, 359.25, 386.75), (15, 0.15625, 386.25)]
[(15, 359.515625, 386.5)]

    # 60cm

    


    