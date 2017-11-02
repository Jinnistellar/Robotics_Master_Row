# Module with code for executing a kick using the Nao's left leg

import Config
import qi
import argparse
import sys
import math
import motion as mot
from naoqi import ALProxy

def left_kick():
    # Handy constants
    TO_RAD = math.pi/180

    # Interfaces with NAO
    motion = Config.motion_service
    posture = Config.posture_service

    memory = Config.memory_service

    # Initialise pose
    posture.goToPosture("StandInit", 0.5)

    # Angle values
    kneeAngle = 40
    torsoAngle = 0
    wideAngle = 0

    #----------------- INITIAL KICKING POSE --------------------
    # Get the number of joints
    NumJoints = len(motion.getJointNames("Body"))

    # Define initial position for kick
    Head     = [0, 0]
    LeftArm  = [120,  15, -90, -80]
    LeftLeg  = [0,  wideAngle, -kneeAngle/2-torsoAngle, kneeAngle, -kneeAngle/2, -wideAngle]
    RightLeg = [0, -wideAngle, -kneeAngle/2-torsoAngle, kneeAngle, -kneeAngle/2,  wideAngle]
    RightArm = [120, -15,  90,  80]

    # If hands are in motion.getJointNames, need to add angles for these
    if (NumJoints == 26):
        LeftArm  += [0, 0]
        RightArm += [0, 0]

    # Combine all joints into a list and convert to radians
    pTargetAngles = Head + LeftArm + LeftLeg + RightLeg + RightArm
    pTargetAngles = [ x * TO_RAD for x in pTargetAngles]

    # Display the starting position
    # print motion.getSummary()
    # print "Left foot sensors values are:"
    # print memory.getData("Device/SubDeviceList/LFoot/FSR/FrontLeft/Sensor/Value")
    # print memory.getData("Device/SubDeviceList/LFoot/FSR/FrontRight/Sensor/Value")
    # print memory.getData("Device/SubDeviceList/LFoot/FSR/RearLeft/Sensor/Value")
    # print memory.getData("Device/SubDeviceList/LFoot/FSR/RearRight/Sensor/Value")

    # More definitions
    pNames = "Body"     # signifies all joints
    pMaxSpeedFraction = 0.2

    # Execute specified motion (initial position)
    motion.angleInterpolationWithSpeed(pNames, pTargetAngles, pMaxSpeedFraction)

    # Display the end position
    # print motion.getSummary()
    # print motion.getSummary()
    # print "Left foot sensors values are:"
    # print  memory.getData("Device/SubDeviceList/LFoot/FSR/FrontLeft/Sensor/Value")
    # print  memory.getData("Device/SubDeviceList/LFoot/FSR/FrontRight/Sensor/Value")
    # print  memory.getData("Device/SubDeviceList/LFoot/FSR/RearLeft/Sensor/Value")
    # print  memory.getData("Device/SubDeviceList/LFoot/FSR/RearRight/Sensor/Value")

    motion.closeHand('RHand')       # not sure why you included this Yiyang?
    
    # Specifications for arm movement (for balancing)
    useSensors = False
    space = mot.FRAME_ROBOT
    axisMask = 63                 # control all the effector's axes
    isAbsolute = False
    times = 0.8

    LeftArm = [90,  25, -90, -10]		# shoulder pitch/roll, elbow yaw/roll
    LeftArm = [ x * TO_RAD for x in LeftArm]

    RightArm = [90, -25,  90,  10]
    RightArm = [ x * TO_RAD for x in RightArm]

    # Execute motion
    motion.angleInterpolation(
        ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll",
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"],
        LeftArm+RightArm, times, True, _async=True)

    # Move torso
    effector = "Torso"
    path = [-0.001, -0.07, -0.01, 0.0, 0.0, 0.0]
    motion.positionInterpolation(effector, space, path, axisMask, 1.6, isAbsolute)
    space = mot.FRAME_TORSO
    
    #----------------- PRE-KICK POSE --------------------
    ### Swing left leg back, move left arm to the front, right arm to the back
    times = 0.5     
    effector = "LLeg"         
    LeftArm = [61,  25, -90, -10]
    LeftArm = [ x * TO_RAD for x in LeftArm]
    RightArm = [119, -25,  90,  10]
    RightArm = [ x * TO_RAD for x in RightArm]

    # Arms
    motion.angleInterpolation(
        ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll",
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"],
        LeftArm+RightArm, times, True, _async=True)

    # Left leg
    path = [-0.10, 0.00, 0.04, 0.0, 0.0, 0.0]
    motion.positionInterpolation(effector, space, path, axisMask, times, isAbsolute)

    #----------------- FORWARD KICK MOTION --------------------               
    ### Swing left leg forward
    times = 0.3              
    LeftArm = [119,  25, -90, -10]
    LeftArm = [ x * TO_RAD for x in LeftArm]
    RightArm = [61, -25,  90,  10]
    RightArm = [ x * TO_RAD for x in RightArm]

    # Arms
    motion.angleInterpolation(
        ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll",
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"],
        LeftArm+RightArm, times, True, _async=True)

    # Left leg
    path = [0.20, 0.0, 0, 0.0, 0.0, 0]
    motion.positionInterpolation(effector, space, path, axisMask, times, isAbsolute)

    # Return to initial pose
    posture.goToPosture("StandInit", 0.5)


if __name__ == "__main__":

    left_kick()
