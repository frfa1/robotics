import cv2
import numpy as np
from picamera import PiCamera
from time import sleep  # Import the sleep function from the time module

# Initialize the Raspberry Pi camera
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 24

# Create an empty NumPy array to store the captured image
image = np.empty((240, 320, 3), dtype=np.uint8)

# Capture an image from the Raspberry Pi camera
camera.capture(image, 'bgr')
cv2.imwrite('out.png', image)
print("Saved image to out.png")

# Continue with the OpenCV camera feed processing
camera = cv2.VideoCapture(0)
cv2.startWindowThread()

while True:
    ret, image = camera.read()

    if not ret:
        break

    # Apply Gaussian Blur to the image
    blurred_image = cv2.GaussianBlur(image, (15, 15), 0)

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2HSV)

    lower_color = np.array([30, 150, 50])  # Change the colors to your preferences
    upper_color = np.array([60, 255, 255])

    # Create a mask to threshold the frame
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check if any detected contour meets the size criteria
    for contour in contours:
        # contourArea calculates the approximate size of the found contour
        area = cv2.contourArea(contour)

        if area > 100:
            print("Found the tennis ball")
        else:
            print("Found something small and yellow")

    # Display the camera feed with detection results
    cv2.imshow('mygrabbed image', mask)
    cv2.waitKey(1)

# Release the camera and close the OpenCV window
camera.release()
cv2.destroyAllWindows()
