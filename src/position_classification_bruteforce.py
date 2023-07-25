import  json
from BodyPoseDetectionSansCVZone.src.pose import Pose
import numpy as np
from numpy import array
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt


def read_pose_data_from_file(file_path):
    with open(file_path, 'r') as file:
        angle_string = file.read()
        try:
            angle_dict = json.loads(angle_string)

            file.close()
        except (ValueError, SyntaxError) as e:
            print("Error while parsing the data:", e)
            return None

    return angle_dict

poses = []
angle_dict = read_pose_data_from_file("output/suiteangletest1.json")

j=0
for i in range(len(angle_dict)):
    temp = angle_dict[str(i)]
    print(i)
    if (((-10 < temp["RightHip"]['x'] < 10) and (45 < temp["RightHip"]['y'] < 65) and (-10 < temp["RightHip"]['z'] < 10)) and 
        ((-25 < temp["RightKnee"]['x'] < -5) and (75 < temp["RightKnee"]['y'] < 95) and (-10< temp["RightKnee"]['z'] < 10)) and
        ((-10 < temp["LeftHip"]['x'] < 10) and (80< temp["LeftHip"]['y'] < 110) and (-10 < temp["LeftHip"]['z'] < 10)) and
        ((-30 < temp["LeftKnee"]['x'] < -15) and (75 < temp["LeftKnee"]['y'] < 95) and (-10< temp["LeftKnee"]['z'] < 10))):
        if i-j > 15 :
            print("")
            print("")
            print("Forward, weight leg : left")
            current_pose = Pose("Forward","straight","left","north",3,0)
            poses.append(current_pose)
            print("")
            print("")
        j=i
        
    elif (((-20 < temp["LeftHip"]['x'] < 0) and (-40 < temp["LeftHip"]['y'] < -20) and (-10 < temp["LeftHip"]['z'] < 10)) and 
        ((-30 < temp["LeftKnee"]['x'] < -10) and (45 < temp["LeftKnee"]['y'] < 65) and (-10< temp["LeftKnee"]['z'] < 10))):
        if i-j > 15 :
            print("")
            print("")
            print("Forward, weight leg : right")
            current_pose = Pose("Forward","straight","right","north",3,0)
            poses.append(current_pose)
            print("")
            print("")        
        j=i
        """ 
        if (((30 < temp["RightHip"]['x'] < 50) and (-85 < temp["RightHip"]['y'] < -70) and (-10 < temp["RightHip"]['z'] < 10)) and 
            ((-50 < temp["RightKnee"]['x'] < -20) and (65 < temp["RightKnee"]['y'] < 80) and (-10< temp["RightKnee"]['z'] < 10))):
            if i-j > 15 :
                print("")
                print("")
                print("Forward, weight leg : left")
                current_pose = Pose("Forward","straight","left","north",3,0)
                poses.append(current_pose)
                print("")
                print("")
            j=i
            
        elif (((-60 < temp["LeftHip"]['x'] < -40) and (-190 < temp["LeftHip"]['y'] < -170) and (-10 < temp["LeftHip"]['z'] < 10)) and 
            ((-50 < temp["LeftKnee"]['x'] < -20) and (70 < temp["LeftKnee"]['y'] < 80) and (-10< temp["LeftKnee"]['z'] < 10))    ):
            if i-j > 15 :
                print("")
                print("")
                print("Forward, weight leg : right")
                current_pose = Pose("Forward","straight","right","north",3,0)
                poses.append(current_pose)
                print("")
                print("")        
            j=i
        
        elif (((70 < temp["RightHip"]['x'] < 90) and (-90 < temp["RightHip"]['y'] < -80)) and 
            ((290 > temp["RightKnee"]['x'] > 265 ) and (85 < temp["RightKnee"]['y'] < 95))):
            if i-j > 15 :
                print("")
                print("")
                print("In air forward, weight leg : left")
                current_pose = Pose("In air forward","straight","left","north",3,0)
                poses.append(current_pose)
                print("")
                print("")
            j=i
        
        elif (((280 <= temp["LeftHip"]['x'] <= 290) and (180 <= temp["LeftHip"]['y'] <= 190)) and 
            ((295 >= temp["LeftKnee"]['x'] >= 285 ) and (85 <= temp["LeftKnee"]['y'] <= 95))):
            if i-j > 15 :
                print("")
                print("")
                print("In air forward, weight leg : right")
                current_pose = Pose("In air forward","straight","right","north",3,0)
                poses.append(current_pose)
                print("")
                print("")
            j=i
        """
    elif (((0 < temp["RightHip"]['x'] < 25) and (5 < temp["RightHip"]['z'] < 35)) and 
        ((-60 < temp["RightKnee"]['x'] < -20) and (25< temp["RightKnee"]['y'] <= 65) and (-5 < temp["RightKnee"]['z'] < 5))    ):
        if i-j > 15 :
            print("")
            print("")
            print("Slide outside, weight leg : left")
            current_pose = Pose("Slide outside","straight","left","north",3,0)
            poses.append(current_pose)
            print("")
            print("")
        j=i

    elif (((-20 < temp["LeftHip"]['x'] < 0) and (75< temp["LeftHip"]['y'] < 100) and (10 < temp["LeftHip"]['z'] < 20)) and 
        ((-30 < temp["LeftKnee"]['x'] < -20) and (-55< temp["LeftKnee"]['y'] < -20) and (-5 < temp["LeftKnee"]['z'] < 5))    ):
        if i-j > 15 :
            print("")
            print("")
            print("Slide outside, weight leg : right")
            current_pose = Pose("Slide outside","straight","right","north",3,0)
            poses.append(current_pose)        
            print("")
            print("")
        j=i
    elif (((-10 < temp["RightHip"]['x'] < 10 ) and (30< temp["RightHip"]['y'] < 45) and (-10 < temp["RightHip"]['z'] < 10)) and 
        ((-45 < temp["RightKnee"]['x'] < -25) and (-75< temp["RightKnee"]['y'] < -65) and (-5 < temp["RightKnee"]['z'] < 5))    ):
        if i-j > 15 :
            print("")
            print("")
            print("Backward, weight leg : left")
            current_pose = Pose("Backward","straight","left","north",3,0)
            poses.append(current_pose)
            print("")
            print("")
        j=i
    elif (((-10 < temp["LeftHip"]['x'] < 10) and (100< temp["LeftHip"]['y'] < 135) and (-15 < temp["LeftHip"]['z'] < 15)) and 
        ((-30 < temp["LeftKnee"]['x'] < -15) and (80< temp["LeftKnee"]['y'] < 90) and (-5 < temp["LeftKnee"]['z'] < 5)) and
        ((-10 < temp["RightHip"]['x'] < 10 ) and (80< temp["RightHip"]['y'] < 90) and (-10 < temp["RightHip"]['z'] < 10))    ):
        if i-j > 15 :
            print("")
            print("")
            print("Backward, weight leg : right")
            current_pose = Pose("Backward","straight","right","north",3,0)
            poses.append(current_pose)        
            print("")
            print("")
        j=i


to_save = ""
for pose in poses :
    """
    Order in the save file for 1 pose :
    Direction
    Height
    Name
    Rotation
    Slider
    Weighted leg
    """
    to_save += str(pose.get_direction_ind)
    to_save += str(pose.get_height_ind)
    to_save += str(pose.get_name_ind)
    to_save += str(pose.get_angle_ind)
    to_save += str(pose.get_slider_ind) 
    to_save += str(pose.get_leg_ind)

print(to_save)
data = bytearray(to_save,'utf-8')

with open("output/bytefile.txt", "wb") as binary_file:
    # Write bytes to file
    binary_file.write(data)

