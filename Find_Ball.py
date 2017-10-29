import Config
import sys
import cv2
import qi
import image
import time
import numpy as np
import math
import Obtain_Image

def look_down():
    """lower the pitch of head to look for ball that is at foot step"""
    print "Start Scanning Field"
    motion_service = Config.motion_service

    # Rotate the HeadPitch joint to a lower angle
    name = "HeadPitch"
    angle = 0.45
    fractionMaxSpeed = 0.2
    motion_service.setAngles(name, angle, fractionMaxSpeed)

    # sleep for 0.5 secs to stabilise motion and avoid blurry pictures
    time.sleep(0.5)

def take_picture():
    Obtain_Image.Init_Camera(1)
    im = Obtain_Image.GetImage()
    im.show()
    im.save("Find_Ball.png", "PNG")


def locate_Ball():
    img = cv2.imread("Find_Ball.png", 1)

    print "Width of the image :" + str(img.shape[1])  # width of image
    print "Height of the image  :" + str(img.shape[0])  # height of image

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #cv2.imshow("HSV Image", hsv)

    lower_orange = np.array([2, 100, 150], np.uint8)
    higher_orange = np.array([25, 255, 255], np.uint8)
    orange = cv2.inRange(hsv, lower_orange, higher_orange)
    #cv2.imshow("Binary Image", orange)

    erode = cv2.erode(orange, None, iterations=1)
    #cv2.imshow("erode Image", erode)

    dilate = cv2.dilate(erode, None, iterations=5)
    #cv2.imshow("dilate Image", dilate)
    #cv2.waitKey()

    smoothing = cv2.blur(orange, (10, 10))
    dilate = cv2.dilate(smoothing, None, iterations=3)
    circles = cv2.HoughCircles(np.asarray(dilate), cv2.HOUGH_GRADIENT, 100, 300, 100, 50)

    # requires 3 inputs
    _, contours, hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    print "Ball_Location_Y-axis : Top to bottom"
    print "Ball_Location_X-axis : Left to right"

    Centre_x, Centre_y, Width, Height, Ball_Location_X, Ball_Location_Y = 0, 0, 0, 0, 0, 0
    Maximum_Diagonal_Length = 0

    for cnt in contours:
        WalkTo_x, WalkTo_y, width, height = cv2.boundingRect(cnt)
        centre_x, centre_y = WalkTo_x + width / 2, WalkTo_y + height / 2

        if 20 < hsv.item(centre_y, centre_x, 0) < 30:
            cv2.rectangle(img, (WalkTo_x, WalkTo_y), (WalkTo_x + width, WalkTo_y + height), [0, 255, 255], 2)
        if (math.sqrt(width * width + height * height) > Maximum_Diagonal_Length):
            Maximum_Diagonal_Length = math.sqrt(width * width + height * height)
            Centre_x, Centre_y, Width, Height, Ball_Location_X, Ball_Location_Y = centre_x, centre_y, width, height, WalkTo_x, WalkTo_y

    # draws rectangle in red then thickness 2
    cv2.rectangle(img, (Ball_Location_X, Ball_Location_Y), (Ball_Location_X + Width, Ball_Location_Y + Height), [0, 23, 255], 2)
    print "CENTER : (" + str(Centre_x) + "," + str(Centre_y) + ") , WIDTH :" + str(Width) + ", HEIGHT :" + str(Height)
    cv2.imshow('Ball detected Image', img)
    cv2.waitKey()

    forward = 0
    horizontal = 0
    use_left_kick = 0

    if (Centre_y < 130):
        print "move one step in front"
        forward= 1

    if(  Centre_x > 524   ):
        horizontal = 2
    if( Centre_x < 524 and Centre_x > 450   ):
        horizontal = 1
    if( Centre_x < 450 and Centre_x > 400  ):
        horizontal = 0.5
    if(Centre_x < 400 and Centre_x > 360):
        horizontal = 0

    if(Centre_x > 320 and Centre_x < 360):
        horizontal = -0.5
        use_left_kick = 1
    if(Centre_x < 130):
        horizontal = -2
        use_left_kick = 1
    if(Centre_x > 130 and Centre_x < 220):
        horizontal = -1
        use_left_kick = 1

    print [horizontal,forward , use_left_kick]

    WalkTo_x = 0.0
    WalkTo_y = -0.05
    theta = 0.0

    # parameters are set to the default value
    Config.motion_service.walkTo(WalkTo_x, WalkTo_y*horizontal , theta, [["StepHeight", 0.02]])

    return [horizontal , forward , use_left_kick]

if __name__ == "__main__":

    WalkTo_x = 0.0
    WalkTo_y = -0.00
    theta = 0.0

    # parameters are set to the default value
    Config.motion_service.walkTo(x, y, theta, [["StepHeight", 0.02]])

    look_down()
    take_picture()
    locate_Ball()