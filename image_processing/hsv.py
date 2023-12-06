import cv2
import numpy as np

# Load the image from file
image_path = '/home/alexander180/Desktop/ITU/Advanced_robotics/robotics/image_processing/photorobot.png'  # Replace with your image path
image = cv2.imread(image_path)

# Convert the image to HSV color space
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define the coordinates of the red circle area (you will need to adjust these)
# For example: top left corner (x, y) and the width and height (w, h) of the bounding box
x, y, w, h = 50, 10, 40, 40  # Replace with the actual coordinates of the red circle

# Crop the image to the red circle area
cropped_image = hsv_image[y:y+h, x:x+w]

# Calculate the average HSV values of the cropped area
average_hsv = np.mean(cropped_image, axis=(0, 1))

# Define a reasonable tolerance for the HSV range
tolerance = np.array([10, 40, 40])  # Example tolerance values for H, S, and V

# Calculate the lower and upper bounds for the HSV values
lower_hsv = np.maximum(average_hsv - tolerance, 0)
upper_hsv = np.minimum(average_hsv + tolerance, [179, 255, 255])

print('Lower HSV Bound:', lower_hsv)
print('Upper HSV Bound:', upper_hsv)
