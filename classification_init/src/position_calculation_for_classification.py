import cv2
import mediapipe as mp
import numpy as np
import math
import json
from scipy.spatial.transform import Rotation

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

############################################################################################################################################
############################################################ PLOTING METHOD  ###############################################################
############################################################################################################################################

def set_axes_equal(ax):
    '''Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc..  This is one possible solution to Matplotlib's
    ax.set_aspect('equal') and ax.axis('equal') not working for 3D.

    Input
    ax: a matplotlib axis, e.g., as output from plt.gca().
    '''

    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    y_range = abs(y_limits[1] - y_limits[0])
    z_range = abs(z_limits[1] - z_limits[0])

    # The plot bounding box is a sphere in the sense of the infinity
    # norm, hence I call half the max range the plot radius.
    plot_radius = 0.5*max([x_range, y_range, z_range])

    ax.set_xlim3d([x_range/2 - plot_radius, x_range/2 + plot_radius])
    ax.set_ylim3d([y_range/2 - plot_radius, y_range/2 + plot_radius])
    ax.set_zlim3d([z_range/2 - plot_radius, z_range/2 + plot_radius])


def normalized_to_pixel_coordinates(
    normalized_x: float, normalized_y: float, image_width: int,
    image_height: int):
  """Converts normalized value pair to pixel coordinates."""

  # Checks if the float value is between 0 and 1.
  def is_valid_normalized_value(value: float) -> bool:
    return (value > 0 or math.isclose(0, value)) and (value < 1 or
                                                      math.isclose(1, value))

  if not (is_valid_normalized_value(normalized_x) and
          is_valid_normalized_value(normalized_y)):
    # TODO: Draw coordinates even if it's outside of the image bounds.
    return None,None
  x_px = min(math.floor(normalized_x * image_width), image_width - 1)
  y_px = min(math.floor(normalized_y * image_height), image_height - 1)
  return x_px, y_px

def draw_coordinate_system(articulation,coordinate_system):

    O,OX,OY,OZ,_ = coordinate_system[articulation]

    Ox,Oy = O[:2]
    OXx,OXy = OX[:2]+O[:2]
    OYx,OYy = OY[:2]+O[:2]
    OZx,OZy = OZ[:2]+O[:2]


    #normalization to plot on cv
    Ox_n,Oy_n = normalized_to_pixel_coordinates(Ox,Oy,width,height)
    OXx_n,OXy_n = normalized_to_pixel_coordinates(OXx,OXy,width,height)
    OYx_n,OYy_n = normalized_to_pixel_coordinates(OYx,OYy,width,height)
    OZx_n,OZy_n = normalized_to_pixel_coordinates(OZx,OZy,width,height)

    #plot
    cv2.line(img,(Ox_n,Oy_n),(OXx_n,OXy_n),(0, 0, 255),thickness = 10)
    cv2.line(img,(Ox_n,Oy_n),(OYx_n,OYy_n),(0, 255, 0),thickness = 10)
    cv2.line(img,(Ox_n,Oy_n),(OZx_n,OZy_n),(255, 0, 0),thickness = 10)

def plot_coordinate_system(coordinate_system):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.scatter3D(lmList[:,0],lmList[:,1],lmList[:,2], cmap='Greens')
    ax.scatter3D(new_lmList[:,0],new_lmList[:,1],new_lmList[:,2], cmap='Greens')
    """
    ax.text3D(coordinate_system[1][0]+coordinate_system[0][0],
            coordinate_system[1][1]+coordinate_system[0][1],
            coordinate_system[1][2]+coordinate_system[0][2],"X")
    ax.text3D(coordinate_system[2][0]+coordinate_system[0][0],
            coordinate_system[2][1]+coordinate_system[0][1],
            coordinate_system[2][2]+coordinate_system[0][2],"Y")
    ax.text3D(coordinate_system[3][0]+coordinate_system[0][0],
            coordinate_system[3][1]+coordinate_system[0][1],
            coordinate_system[3][2]+coordinate_system[0][2],"Z")
    
    ax.plot3D([coordinate_system[0][0],coordinate_system[1][0]+coordinate_system[0][0]],
            [coordinate_system[0][1],coordinate_system[1][1]+coordinate_system[0][1]],
            [coordinate_system[0][2],coordinate_system[1][2]+coordinate_system[0][2]],c="Blue")
    ax.plot3D([coordinate_system[0][0],coordinate_system[2][0]+coordinate_system[0][0]],
            [coordinate_system[0][1],coordinate_system[2][1]+coordinate_system[0][1]],
            [coordinate_system[0][2],coordinate_system[2][2]+coordinate_system[0][2]],c="Blue")
    ax.plot3D([coordinate_system[0][0],coordinate_system[3][0]+coordinate_system[0][0]],
            [coordinate_system[0][1],coordinate_system[3][1]+coordinate_system[0][1]],
            [coordinate_system[0][2],coordinate_system[3][2]+coordinate_system[0][2]],c="Blue")"""
    set_axes_equal(ax)
    plt.savefig(f'frame_{frame}.png')
    plt.show()



############################################################################################################################################
###################################################### COORDINATE SYSTEM COMPUTATION  ######################################################
############################################################################################################################################

POSE_ARTICULATIONS = {
    14:(12,14,16), 13:(11,13,15), 24:(12,24,26), 23:(11,23,25), 26:(24,26,28), 25:(23,25,27),
    28:(26,28,32), 27:(25,27,31), 12:(24,12,11)
}

def coordinate_system_initialisation(lmList,articulation):
   
    p1 = POSE_ARTICULATIONS[articulation][0]
    p2 = POSE_ARTICULATIONS[articulation][1]
    p3 = POSE_ARTICULATIONS[articulation][2]

    O = np.array([lmList[p2,0],lmList[p2,1],lmList[p2,2]])
    OY = np.array([lmList[p1,0],lmList[p1,1],lmList[p1,2]]) - O
    norm_OY = np.linalg.norm(OY)
    if np.linalg.norm(OY) !=0 : 
        OY = OY / norm_OY
    temp = O - np.array([lmList[p3,0],lmList[p3,1],lmList[p3,2]]) 
    
    OZ = np.cross(temp,OY)
    if np.linalg.norm(OZ) !=0 : 
        OZ = OZ / np.linalg.norm(OZ)
    
    OX = np.cross(OY,OZ)
    if np.linalg.norm(OZ) !=0 : 
        OX = OX / np.linalg.norm(OX)
    P = np.array([[OX[0],OY[0],OZ[0]],
                [OX[1],OY[1],OZ[1]],
                [OX[2],OY[2],OZ[2]]])

    newList = (P@(lmList.T-np.expand_dims(O,axis=1))).T
    newList = newList / norm_OY
    return newList,[O,OX,OY,OZ,P]  


############################################################################################################################################
################################################################ VIDEO PROCESSING  #########################################################
############################################################################################################################################

def process_image(image_path, all_poses, nompose):
    with mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as pose:
        video = cv2.VideoCapture(image_path)
        width,height = video.get(cv2.CAP_PROP_FRAME_WIDTH),video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        n = 33
        frame = 0
        success,img = video.read()
        if success:

            #recolor the image
            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            img.flags.writeable = False

            #detect the pose
            results = pose.process(img)

            #recolor the image
            img.flags.writeable = True
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            lmList = np.zeros((n,3))

            #landmark extraction
            try :
                landmarks = results.pose_landmarks.landmark
                for i in range(len(landmarks)):
                    lmList[i,0] = landmarks[i].x*10
                    lmList[i,1] = landmarks[i].y*10
                    lmList[i,2] = landmarks[i].z*10
            except : 
                pass

            # render detection
            mp_drawing.draw_landmarks(img,results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(245,117,66),thickness=2,circle_radius=2),
                        mp_drawing.DrawingSpec(color=(245,66,230),thickness=2,circle_radius=2))


            new_lmList,coordinate_system = list(coordinate_system_initialisation(lmList,12))
            # .tolist() cause ndarray aren't JSON Serializable
            if not np.any(np.isnan(new_lmList)):
                all_poses[nompose] = new_lmList[23:,:].tolist()

            print(lmList)
            print("")
            print(new_lmList)

            #adding each angle of articulation to a dictionnary
            #print(new_lmList)
            img = cv2.resize(img, (960, 540)) 


            cv2.imshow('image',img)

            frame += 1 
            cv2.waitKey(100)  
        else : 
            process = False

	#free the windows
    cv2.destroyAllWindows()
    video.release()
	

all_poses={}
# Read pose names from a file.
with open("input/pose_names.txt", 'r') as file:
	pose_names = [line.strip() for line in file]

# Process each image.
for i in range(8037, 8093):
	image_path = f"input/image0{i}.jpeg"
	nompose = pose_names[i - 8037]  # Get corresponding pose name.
	print(i-8036,nompose)
	process_image(image_path, all_poses, nompose)
        
# Write poses back to file.
all_poses_string = str(all_poses)
with open("output/position_for_classification.json", 'w') as file:
	json.dump(all_poses,file)	
