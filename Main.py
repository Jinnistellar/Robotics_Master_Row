import Config
import Find_Goal
import Find_Ball
import Left_Kick
import Right_Kick
import time
import numpy as np
import math
from naoqi import ALProxy

if __name__ == "__main__":

    angle = Find_Goal.scan_field()

    motion = Config.motion_service

    motion.moveTo(0.0, 0.0, angle)
    time.sleep(2)

    Find_Ball.look_down()
    Find_Ball.take_picture()
    a = Find_Ball.locate_Ball()
    if(a[2]):
        Left_Kick.left_kick()
    else:
        Right_Kick.right_kick()

    Config.voice_service.say("Yay, I have scored a goal, in your face")