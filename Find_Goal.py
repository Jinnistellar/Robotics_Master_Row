import Config
import sys
import cv2
import qi
import image
import time
import numpy as np
import math
import Obtain_Image

def find_angle_to_turn( detected_goal_list ):
    print "-----------Start finding turning angle needed to face the goal-----------------"
    min_distance_from_centre = 1000
    angle_to_turn = 0

    for i in detected_goal_list:
        if(i[1]< min_distance_from_centre and i[2] > 300 ) :
            min_distance_from_centre = i[1]
            angle_to_turn = i[4]

    print angle_to_turn
    print "-----------Finished finding turning angle needed to face the goal---------------"
    return angle_to_turn


def scan_field():

    print "Start Scanning Field"
    motion_service = Config.motion_service

    Obtain_Image.Init_Camera(0)

    # set the head to face the centre
    names = ["HeadYaw", "HeadPitch"]
    angles = [0.0, 0.0]
    fractionMaxSpeed = 0.2
    motion_service.setAngles(names, angles, fractionMaxSpeed)

    # Rotate the HeadYaw joint to scan the field
    HEADYAW = "HeadYaw"
    HEADPITCH = "HeadPitch"
    # Rotation range in rad starts from -1.08 to +1.08, therefore total range is 2.16
    rotation_range = 2.16
    # number of steps takes to scan the field
    number_of_division = 10
    increment = rotation_range / number_of_division

    # list containing the parameters returned from find_goal() function.
    detected_goal_list = []

    for i in range(number_of_division + 1):
        # starting from the right most angle---> divide rotation range by half and take minus
        angle = -rotation_range/2 + increment * i

        motion_service.setAngles(HEADYAW, angle, fractionMaxSpeed)
        print "Looking at angle:" + str(angle)

        head_pitch_angle = -0.15
        motion_service.setAngles(HEADPITCH, head_pitch_angle, fractionMaxSpeed)

        # sleep for 1 sec to stabilize motion so that blurry image can be avoided
        time.sleep(1.0)
        im = Obtain_Image.GetImage()

        picture_name = "camImage" + str(angle) + ".PNG"
        im.save(picture_name, "PNG")

        temp = find_goal(picture_name)
        temp.append(angle)
        detected_goal_list.append(temp)

        print "-----------------------------------------------------------------"

    # reset the head to initial position
    angles = [0.0, 0.0]
    fractionMaxSpeed = 0.2
    motion_service.setAngles(names, angles, fractionMaxSpeed)

    print "Finished Scanning Field"

    return find_angle_to_turn(detected_goal_list)


def find_goal(picture_name):
    """detect the goal in a given picture
    :param picture_name:
    :return:    1. distance between centre of max rectangle and centre of the picture
                2. diagonal distance of the max rectangle found in the picture
                3. width of the max rectangle found
                4. height of the max rectangle found
    """
    img = cv2.imread(picture_name, cv2.IMREAD_COLOR)
    width = img.shape[1]
    height = img.shape[0]
    print "Width of the image :" + str(width)
    print "Height of the image :" + str(height)

    # convert the BGR image to HSV format
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # cv2.imshow("HSV Image", hsv)

    # create numpy array representing the range of HSV value
    lower_yellow = np.array((0, 100, 80), np.uint8)
    higher_yellow = np.array((180, 255, 255), np.uint8)

    # use cv2.inRange function to extract thee yellow part of the picture
    yellow = cv2.inRange(hsv, lower_yellow, higher_yellow)
    # cv2.imshow("Binary Image", yellow)

    # erosion and dilation to bring the segmented image together
    erode = cv2.erode(yellow, None, iterations=2)
    # cv2.imshow("erode Image", erode)

    dilate = cv2.dilate(erode, None, iterations=3)
    # cv2.imshow("dilate Image", dilate)

    # requires 3 inputs
    _, contours, hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # print "Ball_Location_Y-axis : Top to bottom"
    # print "Ball_Location_X-axis : Left to right"

    Centre_X, Centre_Y, Width, Height, Ball_Location_X, Ball_Location_Y = 0, 0, 0, 0, 0, 0

    Maximum_Diagonal = 0

    # iterate through all the contour points to get the contour that gives a maximum rectangle
    for cnt in contours:
        x, y, width, height = cv2.boundingRect(cnt)
        centre_x, centre_y = x + width / 2, y + height / 2

        if (math.sqrt(width * width + height * height) > Maximum_Diagonal):
            Maximum_Diagonal = math.sqrt(width * width + height * height)
            Centre_X, Centre_Y, Width, Height, Ball_Location_X, Ball_Location_Y = centre_x, centre_y, width, height, x, y

    # draw the maximum rectangle on top of the image
    cv2.rectangle(img, (Ball_Location_X, Ball_Location_Y), (Ball_Location_X + Width, Ball_Location_Y + Height), [0, 23, 255], 2)
    distance_from_centre = math.sqrt(abs(Centre_X - width / 2) * abs(Centre_X - width / 2) + abs(Centre_Y - height / 2) * abs(Centre_Y - height / 2))

    print "CENTER Location--" + " Ball_Location_X:" + str(Centre_X) + "  Ball_Location_Y: " + str(Centre_Y) + " , WIDTH :" + str(Width) + ", HEIGHT :" + str(Height)
    print "Maximum Diagonal :" + str(Maximum_Diagonal)
    print "Distance from centre: " + str(distance_from_centre)


    # cv2.imshow('goal detected Image', img)
    # cv2.waitKey()

    #img.save(picture_name, "PNG")

    return [distance_from_centre, Maximum_Diagonal, Width, Height]


if __name__ == "__main__":

    scan_field()
