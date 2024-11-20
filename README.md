# Repository related to Advanced Robotics Course @ IT University of Copenhagen

In the exam project, we developed Seeker and Avoider controls for a autonomous 4-wheeled robot. 

The goal of the Seeker was to detect Avoider-robots using sensors like infrared sensors and coded behavior, and chase them down. This was done using an unsupervised Q-learning algorithm with different sensor-based states and behaviors. The Q-learning was simulated to generate much training data without the need of many physical runs of the robot.

For both of the behaviors, the robot had to stay within an area marked by borders. For the Avoider, which had to avoid getting caught by the Seeker-robot, we tried strategies such as following the border line.

See more detailed explaination at the [**report**](https://github.com/frfa1/robotics/blob/main/report.pdf).
