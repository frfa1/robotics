import cv2
import numpy as np


# Initialize the camera (0 is typically the default camera on a lapt
camera = cv2.VideoCapture(0)

cv2.startWindowThread()

while True:

    ret, image = camera.read()

    if not ret:
        break

# Blue to filter out noise
blurred_image = cv2.GaussianBlur, (image(15, 15), 0)
# Convert the frame to HSV colour space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower_color = np.array([30, 150, 50])
upper_color = np.array([60, 255, 255])

# Create a mask to threshold the frame
mask = cv2.inRange(hsv, lower_color, upper_color)


# Find contours in the mask
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                               cv2.CHAIN_APPROX_SIMPLE)
# Check if any detected contour meets the size criteria
for contour in contours:
    # contourArea calculates the approximate size of the found contour
    area = cv2.contourAre(contour)

    if area > 100:
        print("found the tennis ball")
    else:
        print("found something small and yello")


# Display the camera feed with detection results
cv2.imshow('mygrabbed image', mask)
cv2.waitKey(1)

# Release the camera and close the OpenCv window

camera.release()
cv2.destroyAllWindows()
