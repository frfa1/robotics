import cv2
import numpy as np

# Specify the device path for the external camera
external_camera_path = '/dev/video2'

# Initialize the camera using the specified path
camera = cv2.VideoCapture(external_camera_path)

cv2.startWindowThread()

while True:
    ret, image = camera.read()

    if not ret:
        break

    # Create a black background image with the same dimensions as the captured frame
    black_background = np.zeros(image.shape, dtype=np.uint8)

    # Apply Gaussian Blur to the image
    blurred_image = cv2.GaussianBlur(image, (15, 15), 0)

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2HSV)

    # Specify the color range for blue
    lower_color = np.array([90, 50, 50])
    upper_color = np.array([130, 255, 255])

    # Create a mask to threshold the frame for the specified color
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Find contours in the mask
    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check if any detected contour meets the size criteria
    for contour in contours:
        # contourArea calculates the approximate size of the found contour
        area = cv2.contourArea(contour)

        if area > 100:
            # Draw a bounding box around the detected object (green color)
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green color

    # Display the camera feed with detection results
    cv2.imshow('Object Detection', image)  # Show the original image with green rectangles
    cv2.waitKey(1)

# Release the camera and close the OpenCV window
camera.release()
cv2.destroyAllWindows()
