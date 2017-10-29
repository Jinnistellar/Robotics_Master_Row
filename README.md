# Robotics_Master_Row

Welcome to Row Row Row your Bot, oh BUOY, aren't you in for a treat, I hope you get reeled in by our excitement! It is aboat time we get started, and first we will get anchored into the intro of each code file. It is anchor-aged to read this before running the code to get an idea of how it runs, i hope you do knot try to run it because you may not have a crew aboat it...but you know how it is sometimes with pier pressure.

I mast as-shore you, it won't go off course and will be "Pacific". I wreck-en it would be interesting oar even, it might coarse a sea-zure
Anyhow, i shoal carry on and you know what the saying is.. lets "Seas the day!"


Config:
         1) Creating connection to Nao and error if cannot
         2) Listing of services used to operate Nao (motion, camera, memory, voice, posture)
p2:

Main:
         1) Using all codes to implement the actual task
         2) Finding angle so that Nao knows where to move to
         3) Depending on where the ball is, Left kick or Right kick
         4) Voice command: Yay, i have scored a goal, in your face!
              
Obtain_Image:
         1) Creates proxy for camera imaging and using vision definitions as its reference
         2) Specifying resolution and colourspace, and subscribing to the videoclient
           
vision_definitions:
         1) For Obtain_Image

Find_Goal:
Here, our objective is:
         1) Find the angle to turn towards and face the goal
         2) Scan the field
                - Using HeadYaw and HeadPitch to scan the field in increments, stop for a bit to adjust, then retrieve image
         3) Find goal
                - Distance between centre of maximum rectangle and centre of picture
                - Diagonal distance of the maximum recntage found in picture
                - Width and height of max rectangle found
                - Using colour range of yellow can be used to extract yellow parts of the picture
                - Then use erode/dilate to bring the segemented images together
                - Find contours of the goal, and then to draw a rectangle around it

Find_Ball:
Here, our objective is:
         1) Look down for ball:
                - By lowering pitch of head to look for ball that is infront of the foot
         2) Take picture:
                - Obtain image and save image as  "Find_Ball"
         3) Locate ball:
                - Using saved image "Find_Ball", read so that it can convert RGB to HSV
                - Using colour range of orange can be used to extract orange parts of the picture
                - Then use erode/dilate to bring the segemented images together
                - Find contours of the ball, and then to draw a rectangle around it

Left_Kick/Right_kick:
         1) Using proxy for motion
         2) 



