import  json
from visualtangovisionupdate.src.pose import Pose
import numpy as np
from numpy import array
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt


def read_pose_data_from_file(file_path):
    with open(file_path, 'r') as file:
        position_string = file.read()
        try:
            position_dict = json.loads(position_string)

            file.close()
        except (ValueError, SyntaxError) as e:
            print("Error while parsing the data:", e)
            return None

    return position_dict

def dict2array(dictionnary):
    sup_keys = list(dictionnary.keys())
    sub_keys = list(dictionnary[sup_keys[0]].keys())
    n,p = len(sup_keys),len(sub_keys)
    res = np.zeros((n,p))
    for col in range(p):
        for row in range(n):
            #print(f"dictionnary[sup_keys[row]] : {dictionnary[sup_keys[row]]}")
            res[row,col] = dictionnary[sup_keys[row]][sub_keys[col]]
    return res

def frobenius(mat1,mat2):
            return np.linalg.norm(mat1-mat2,'nuc')

if __name__ == "__main__":
    print('Voulez-vous classer selon les coordonnées 3D ou les angles ?')
    print("Veuillez entrer 'pos' ou 'angle'")
    todo = str(input())
    poses = []
    if todo == "pos" :
        position_dict = read_pose_data_from_file("output/suiteposition.json")
        position_for_classification = read_pose_data_from_file("classification_init/output/position_for_classification.json")
        
        for frame in range(len(position_dict)):
            print(frame)
            dist = frobenius(np.array(position_dict[str(frame)]),np.array(position_for_classification["Pose('Collected','straight','right','north',3,0)"]))
            res = Pose("Collected","straight","right","north",3,0)
            #a=np.array([frobenius(angle_dict[frame],angle_for_classification[i]) for i in range(len(angle_for_classification)))

            for pose,positions in position_for_classification.items():
                #print('pose'+str(pose))
                temp  = frobenius(np.array(position_dict[str(frame)]),np.array(position_for_classification[pose]))
                print(temp)
                if temp < dist : 
                    dist = temp
                    res = pose
                #print('res'+str(res))
            print(res)
            poses.append(eval(res))
    elif todo == "angle":
        angle_dict = read_pose_data_from_file("output/suiteangle.json")
        angle_for_classification = read_pose_data_from_file("classification_init/output/angle_for_classification.json")
        j = 0
        for frame in range(len(angle_dict)):
            print(frame)
            dist = frobenius(dict2array(angle_dict[str(frame)]),dict2array(angle_for_classification["Pose('Collected','straight','right','north',3,0)"]))
            res = Pose("Collected","straight","right","north",3,0)
            #a=np.array([frobenius(angle_dict[frame],angle_for_classification[i]) for i in range(len(angle_for_classification)))

            for pose,angle in angle_for_classification.items():
                #print('pose'+str(pose))
                temp  = frobenius(dict2array(angle_dict[str(frame)]),dict2array(angle_for_classification[pose]))
                if temp < dist : 
                    dist = temp
                    res = pose
                    toprint = angle
                #print('res'+str(res))
            
            if frame - j > 15 :
                print(res)
                print(print(toprint))
                poses.append(eval(res))
                print()
                j = frame



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


    #TODO : Dictionnaire des positions.


    """
    vitesse 0 => 1,20 secondes / 2905 avec pauses
    vitesse 1 => 0,79 secondes / 1,20 avec pauses 
    vitesse 2 => 0,71 secondes / 0,57 avec pauses
    vitesse 3 =>   / 0,465 avec pauses
    vitesse 4 =>  / 0,3025 avec pauses
    vitesse 5 =>  /0,25 avec pauses
    vitesse 6 => 
    vitesse 7 => 
    """


    