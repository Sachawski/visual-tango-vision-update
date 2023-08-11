import numpy as np
import ast
from src.pose import Pose
from src.tomatrix import pose_to_matrix

def frobenius(mat1,mat2):
	return np.linalg.norm(mat1-mat2,'fro')
	
def angle_classification(poses,all_poses):
	with open("/static/output/angle_for_classification.txt", 'r') as file:
		angle_for_classification = file.read()
		angle_for_classification = ast.literal_eval(angle_for_classification)
		file.close() 
		for key,value in all_poses.items() :
			L=[(i,frobenius(pose_to_matrix(all_poses["Test"]),pose_to_matrix(angle_for_classification[i]))) for i in angle_for_classification.keys()]
            # Code pour exécuter le programme Python avec le fichier d'entrée
            # Enregistrer le fichier de sortie
			s=""
			L.sort(key=lambda x: x[1])
			for item in L:
				s+=f'{item[0]}: {item[1]}\n'
			poses.append(eval(L[0][0]))		
		to_save = ""
		for pose in poses:
			to_save += str(pose._d)
			to_save += str(pose.get_height_ind)
			to_save += str(pose.get_name_ind)
			to_save += str(pose.get_angle_ind)
			to_save += str(pose.get_slider_ind) 
			to_save += str(pose.get_leg_ind)
        
		data = bytearray(to_save,'utf-8')
	with open("/static/temp/save.txt", "wb") as output_file:
        	output_file.write(data)
	return s
