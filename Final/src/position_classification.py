import ast

import numpy as np



def frobenius(mat1,mat2):
    return np.linalg.norm(mat1-mat2,'fro')
"""
def dict2array(dic):
    all_keys = dic.keys()
    n,p = len(dic),len(dic[all_keys[0]])
    res = np.zeros((n,p))
    for i in range(n):
        for j in range(p):
            sub_keys = dict[all_keys[i]].keys()
            res[i,j]= dict[all_keys[i]][sub_keys[j]]
    return res

print(dict2array(angle_for_classification[1]))
"""
if __name__ == '__main__':
    with open("output/suiteangle.txt", 'r') as file:
        anglestring = file.read()
    angle_dict = ast.literal_eval(anglestring)
    file.close()

    with open("output/angle_for_classification.txt", 'r') as file:
        angle_for_classification = file.read()
    angle_for_classification = ast.literal_eval(angle_for_classification)
    file.close()

    poses = []
    for frame in range(len(angle_dict)):
        dist = frobenius(angle_dict[frame],angle_for_classification['Pose("Collected","straight","right","north",3,0)'])
        res = Pose("Collected","straight","right","north",3,0)
        #a=np.array([frobenius(angle_dict[frame],angle_for_classification[i]) for i in range(len(angle_for_classification)))

        for pose,positions in angle_for_classification.items():
            temp  = frobenius(angle_dict[frame],angle_for_classification[pose])
            if temp < dist : 
                dist = temp
                res = pose
        poses.append(eval(res))



    #TODO : Dictionnaire des positions.
    #poses = {Pose("Forward","straight","left","north",3,0)}
    """
    print('debut')
    j=0
    for i in range(len(angle_dict)):
        temp = angle_dict[i]
        if (((30 < temp["RightHip"]['x'] < 50) and (-85 < temp["RightHip"]['y'] < -70) and (-10 < temp["RightHip"]['z'] < 10)) and 
            ((-30 > temp["RightKnee"]['x'] > 0 or 325 > temp["RightKnee"]['x'] > 300 ) and (65 < temp["RightKnee"]['y'] < 80) and (-10< temp["RightKnee"]['z'] < 10))    ):
            if i-j > 15 :
                print("")
                print("")
                print("Forward, weight leg : left")
                poses.append(Pose("Forward","straight","left","north",3,0))
                print("")
                print("")
            j=i
        elif (((300 < temp["LeftHip"]['x'] < 310) and (175 < temp["LeftHip"]['y'] < 185) and (-10 < temp["LeftHip"]['z'] < 10)) and 
            ((315 > temp["LeftKnee"]['x'] > 310) and (70 < temp["LeftKnee"]['y'] < 80) and (-10< temp["LeftKnee"]['z'] < 10))    ):
            if i-j > 15 :
                print("")
                print("")
                print("Forward, weight leg : right")
                poses.append(Pose("Forward","straight","right","north",3,0))
                print("")
                print("")        
            j=i
        elif (((70 < temp["RightHip"]['x'] < 90) and (-90 < temp["RightHip"]['y'] < -80)) and 
            ((290 > temp["RightKnee"]['x'] > 265 ) and (85 < temp["RightKnee"]['y'] < 95))):
            if i-j > 15 :
                print("")
                print("")
                print("In air forward, weight leg : left")
                poses.append(Pose("In air forward","straight","left","north",3,0))
                print("")
                print("")
            j=i
        elif (((280 <= temp["LeftHip"]['x'] <= 290) and (180 <= temp["LeftHip"]['y'] <= 190)) and 
            ((295 >= temp["LeftKnee"]['x'] >= 285 ) and (85 <= temp["LeftKnee"]['y'] <= 95))):
            if i-j > 15 :
                print("")
                print("")
                print("In air forward, weight leg : right")
                poses.append(Pose("In air forward","straight","right","north",3,0))
                print("")
                print("")
            j=i
        elif (((20 < temp["RightHip"]['x'] < 30) and (-20< temp["RightHip"]['y'] < -10) and (30 < temp["RightHip"]['z'] < 35)) and 
            ((280 > temp["RightKnee"]['x'] > 260) and (25< temp["RightKnee"]['y'] < 40) and (-5 < temp["RightKnee"]['z'] < 5))    ):
            if i-j > 15 :
                print("")
                print("")
                print("Slide outside, weight leg : left")
                poses.append(Pose("Slide outside","straight","left","north",3,0))
                print("")
                print("")
            j=i

        elif (((340 < temp["LeftHip"]['x'] < 360 or -20 < temp["LeftHip"]['x'] < 0) and (80< temp["LeftHip"]['y'] < 90) and (15 < temp["LeftHip"]['z'] < 25)) and 
            ((340 > temp["LeftKnee"]['x'] > 325) and (325< temp["LeftKnee"]['y'] < 345) and (-5 < temp["LeftKnee"]['z'] < 5))    ):
            if i-j > 15 :
                print("")
                print("")
                print("Slide outside, weight leg : right")
                poses.append(Pose("Slide outside","straight","right","north",3,0))        
                print("")
                print("")
            j=i
        

        elif (((340 < temp["RightHip"]['x'] < 360 or -20 < temp["RightHip"]['x'] < 0) and (-95< temp["RightHip"]['y'] < -105 or 70< temp["RightHip"]['y'] < 80) and (-10 < temp["RightHip"]['z'] < 10)) and 
            ((320 > temp["RightKnee"]['x'] > 300) and (85< temp["RightKnee"]['y'] < 95) and (-5 < temp["RightKnee"]['z'] < 5))    ):
            if i-j > 15 :
                print("")
                print("")
                print("Backward, weight leg : left")
                poses.append(Pose("Backward","straight","left","north",3,0))
                print("")
                print("")
            j=i


        elif (((0 < temp["LeftHip"]['x'] < 40 or -20 < temp["LeftHip"]['x'] < 0) and (10< temp["LeftHip"]['y'] < 30) and (-15 < temp["LeftHip"]['z'] < 15)) and 
            ((-60 > temp["LeftKnee"]['x'] > -85) and (-90< temp["LeftKnee"]['y'] < -70) and (-5 < temp["LeftKnee"]['z'] < 5))):
            if i-j > 15 :
                print("")
                print("")
                print("Backward, weight leg : right")
                poses.append(Pose("Backward","straight","right","north",3,0))        
                print("")
                print("")
            j=i
            
    print('fin')
    """
    print(poses)

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

    data = bytearray(to_save,'utf-8')

    with open("output/bytefile.txt", "wb") as binary_file:
        # Write bytes to file
        binary_file.write(data)