import cv2
import numpy as np

# Specify the device path for the external camera
#external_camera_path = '/dev/video2'

# Initialize the camera using the specified path
#camera = cv2.VideoCapture(external_camera_path)
camera = cv2.VideoCapture(0)

def capture_and_save_image(file_path):
    # Number 0 indicates that we want to capture from the first available camera.
    # If you have more than one camera, you can select the next by replacing 0 with 1, and so forth.

# Initialize the camera (0 is typically the default camera on a laptop)
    camera = cv2.VideoCapture(0)


    if not camera.isOpened():
            print("Error: Couldn't open the camera.")
            return

    # Read the current frame from the video capture
    ret, frame = camera.read()

    cv2.startWindowThread()
    
    if ret:
        # Save the image on disk
        cv2.imwrite(file_path, frame)
        print(f"Image captured and saved at {file_path}")
    else:
        print("Error: Couldn't grab the frame from the camera.")

    while True:
        ret, image = camera.read()

        if not ret:
            break

    # Apply Gaussian Blur to the image
    blurred_image = cv2.GaussianBlur(image, (15, 15), 0)

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2HSV)

    lower_color = np.array([30, 150, 50]) ## change the colours to your preferences
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
            print("found the tennis ball")
        else:
            print("found something small and yellow")

    # Display the camera feed with detection results
    cv2.imshow('mygrabbed image', mask)
    cv2.waitKey(1)

# Release the camera and close the OpenCV window
    camera.release()
    cv2.destroyAllWindows()
