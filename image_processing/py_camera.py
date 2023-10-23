import cv2
import numpy as np
from picamera import PiCamera 


# i n i t i a l i z e
camera = PiCamera()


def testCamera():
    print("Camera test")
    camera.start_preview()
    sleep(5)


# we c a p t u r e t o openCV c om p a t i bl e forma t
1
# you m igh t want t o i n c r e a s e r e s o l u t i o n

camera.resolution = (320, 240)
camera.frameRate = 24

sleep(2)


image = np.empty((240, 320, 3), dtype=np.uint8)


camera.capture(image, 'bgr')
cv2.imwrite('out.png', image)
camera.stoppreview()
print("saved_image_to_out.png")
