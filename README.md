# Robotics_Master_Row

Welcome to Row Row Row your Boat, oh BUOY, aren't you in for a treat, I hope you get reeled in by our excitement! It is aboat time we get started, and first we will get anchored into the intro of each code file. It is anchor-aged to read this before running the code to get an idea of how it runs, i hope you do knot try to run it because you may not have a crew aboat it...but you know how it is sometimes with pier pressure.

I mast as-shore you, it won't go off course and will be "Pacific". I wreck-en it would be interesting oar even, it might coarse a sea-zure
Anyhow, i shoal carry on and you know what the saying is.. lets "Seas the day!"


Config:

p2:

Main:

Obtain_Image:

vision_definitions:

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

Left_Kick:

Right_Kick:



