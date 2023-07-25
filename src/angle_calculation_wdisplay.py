import cv2
import mediapipe as mp
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
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

def plot_coordinate_system():
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    for i in ARTICULATIONS:
        ax.scatter3D(lmList[:,0],lmList[:,1],lmList[:,2], cmap='Greens')
        ax.text3D(coordinate_system[i][1][0]+coordinate_system[i][0][0],
                coordinate_system[i][1][1]+coordinate_system[i][0][1],
                coordinate_system[i][1][2]+coordinate_system[i][0][2],"X")
        ax.text3D(coordinate_system[i][2][0]+coordinate_system[i][0][0],
                coordinate_system[i][2][1]+coordinate_system[i][0][1],
                coordinate_system[i][2][2]+coordinate_system[i][0][2],"Y")
        ax.text3D(coordinate_system[i][3][0]+coordinate_system[i][0][0],
                coordinate_system[i][3][1]+coordinate_system[i][0][1],
                coordinate_system[i][3][2]+coordinate_system[i][0][2],"Z")
        ax.plot3D([coordinate_system[i][0][0],coordinate_system[i][1][0]+coordinate_system[i][0][0]],
                [coordinate_system[i][0][1],coordinate_system[i][1][1]+coordinate_system[i][0][1]],
                [coordinate_system[i][0][2],coordinate_system[i][1][2]+coordinate_system[i][0][2]],c="Blue")
        ax.plot3D([coordinate_system[i][0][0],coordinate_system[i][2][0]+coordinate_system[i][0][0]],
                [coordinate_system[i][0][1],coordinate_system[i][2][1]+coordinate_system[i][0][1]],
                [coordinate_system[i][0][2],coordinate_system[i][2][2]+coordinate_system[i][0][2]],c="Blue")
        ax.plot3D([coordinate_system[i][0][0],coordinate_system[i][3][0]+coordinate_system[i][0][0]],
                [coordinate_system[i][0][1],coordinate_system[i][3][1]+coordinate_system[i][0][1]],
                [coordinate_system[i][0][2],coordinate_system[i][3][2]+coordinate_system[i][0][2]],c="Blue")
    set_axes_equal(ax)
    plt.savefig(f'frame_{frame}.png')



############################################################################################################################################
###################################################### COORDINATE SYSTEM COMPUTATION  ######################################################
############################################################################################################################################


POSE_ARTICULATIONS = {
    14:(12,14,16), 13:(11,13,15), 24:(12,24,26), 23:(11,23,25), 26:(24,26,28), 25:(23,25,27),
    28:(26,28,32), 27:(25,27,31)
}

COORDINATE_SYSTEM_INIT_DICT = {
    24:(12,24,23), 23:(11,23,24)
} 

ARTICULATIONS = set([13,14,24,23,26,25,28,27])

def coordinate_system_initialisation(lmList,articulation):
   
    
    if articulation == 24 or articulation ==23:
        p1 = COORDINATE_SYSTEM_INIT_DICT[articulation][0]
        p2 = COORDINATE_SYSTEM_INIT_DICT[articulation][1]
        p3 = COORDINATE_SYSTEM_INIT_DICT[articulation][2]

        O = np.array([lmList[p2,0],lmList[p2,1],lmList[p2,2]])
        OY = np.array([lmList[p1,0],lmList[p1,1],lmList[p1,2]]) - O

        if np.linalg.norm(OY) !=0 : 
            OY = OY / np.linalg.norm(OY)
        temp = O - np.array([lmList[p3,0],lmList[p3,1],lmList[p3,2]]) 
        
        OZ = np.cross(temp,OY)
        if np.linalg.norm(OZ) !=0 : 
            OZ = OZ / np.linalg.norm(OZ)
        
        OX = np.cross(OY,OZ)
        if np.linalg.norm(OX) !=0 : 
            OX = OX / np.linalg.norm(OX)
        P = np.array([[OX[0],OY[0],OZ[0]],
                    [OX[1],OY[1],OZ[1]],
                    [OX[2],OY[2],OZ[2]]])
    else:
        p1 = POSE_ARTICULATIONS[articulation][0]
        p2 = POSE_ARTICULATIONS[articulation][1]
        p3 = POSE_ARTICULATIONS[articulation][2]

        O = np.array([lmList[p2,0],lmList[p2,1],lmList[p2,2]])
        OY = np.array([lmList[p1,0],lmList[p1,1],lmList[p1,2]]) - O

        if np.linalg.norm(OY) !=0 : 
            OY = OY / np.linalg.norm(OY)
        temp = O - np.array([lmList[p3,0],lmList[p3,1],lmList[p3,2]]) 
        
        OX = np.cross(temp,OY)
        if np.linalg.norm(OX) !=0 : 
            OX = OX / np.linalg.norm(OX)
        
        OZ = np.cross(OX,OY)
        if np.linalg.norm(OZ) !=0 : 
            OZ = OZ / np.linalg.norm(OZ)
        P = np.array([[OX[0],OY[0],OZ[0]],
                    [OX[1],OY[1],OZ[1]],
                    [OX[2],OY[2],OZ[2]]])
    """
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.scatter3D(lmList[:,0],lmList[:,1],lmList[:,2], cmap='Greens')
    ax.plot3D([O[0],OX[0]+O[0]],
                [O[1],OX[1]+O[1]],
                [O[2],OX[2]+O[2]],c="Blue")
    ax.plot3D([O[0],OY[0]+O[0]],
                [O[1],OY[1]+O[1]],
                [O[2],OY[2]+O[2]],c="Red")
    ax.plot3D([O[0],OZ[0]+O[0]],
                [O[1],OZ[1]+O[1]],
                [O[2],OZ[2]+O[2]],c="green")
    set_axes_equal(ax)
    plt.show()"""
    return O,OX,OY,OZ,P     
    
def angle(lmList,articulation,coordinate_system):

    p1 = POSE_ARTICULATIONS[articulation][0]
    p2 = POSE_ARTICULATIONS[articulation][1]
    p3 = POSE_ARTICULATIONS[articulation][2]

    # Définition des points
    A = lmList[p1,:]
    B = lmList[p2,:]
    C = lmList[p3,:]
    P = coordinate_system[articulation][4]


    new_A = P@(A-coordinate_system[articulation][0])
    new_B = P@(B-coordinate_system[articulation][0])
    new_C = P@(C-coordinate_system[articulation][0])
    
    # Calcul des vecteurs
    AB = new_A - new_B
    BC = new_B - new_C
    # Normalisation des vecteurs
    if np.linalg.norm(AB) != 0:
        AB = AB / np.linalg.norm(AB) 
    if np.linalg.norm(BC) != 0:   
        BC = BC / np.linalg.norm(BC) 
    
    # Calcul de l'angle d'Euler dans le plan XY
    angle_xy = np.arctan2(BC[1], BC[0]) - np.arctan2(AB[1], AB[0])
    # Calcul de l'angle d'Euler dans le plan XZ
    angle_xz = np.arctan2(BC[2], BC[0]) - np.arctan2(AB[2], AB[0])

    # Calcul de l'angle d'Euler dans le plan YZ
    angle_yz = np.arctan2(BC[2], BC[1]) - np.arctan2(AB[2], AB[1])
    
    # Conversion des angles en degrés
    angle_xy = np.degrees(angle_xy)
    if angle_xy < 0:
        angle_xy += 360 
    if angle_xy >= 180:
        angle_xy -= 360
    angle_xz = np.degrees(angle_xz)
    if angle_xz < 0:
        angle_xz += 360 
    if angle_xz >= 180:
        angle_xz-= 360
    angle_yz = np.degrees(angle_yz)
    if angle_yz < 0:
        angle_yz += 360 
    if angle_yz >= 180:
        angle_yz -= 360
    print(f"Angle Z: {int(angle_xy)} degrees")
    print(f"Angle Y: {int(angle_xz)} degrees")
    print(f"Angle X: {int(angle_yz)} degrees")
    
    return {"x":angle_yz,"y":angle_xz,"z":angle_xy}


############################################################################################################################################
################################################################ VIDEO PROCESSING  #########################################################
############################################################################################################################################
process = True

#Processing of the video 
with mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as pose:
    #import the video to process
    video = cv2.VideoCapture('input/test1.mp4')
    #video = cv2.VideoCapture('input/test1.mp4')
    width,height = video.get(cv2.CAP_PROP_FRAME_WIDTH),video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    n = 33
    all_angles = {}
    frame = 0
    coordinate_system = {}
    while process:
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
                    lmList[i,2] = landmarks[i].z*10/3
            except : 
                pass

            # render detection
            mp_drawing.draw_landmarks(img,results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245,117,66),thickness=2,circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245,66,230),thickness=2,circle_radius=2))


            
            for articulation in ARTICULATIONS:
                coordinate_system[articulation] = list(coordinate_system_initialisation(lmList,articulation))
            print(frame)
            #adding each angle of articulation to a dictionnary
            angle_dict = {}
            if len(lmList)!=0 :
                #angle_dict["CoudeGauche"],img= angle(lmList,img,11,13,15)
                print("Hanche droite")
                angle_dict["RightHip"]= angle(lmList,24,coordinate_system)
                print("Hanche gauche")
                angle_dict["LeftHip"] = angle(lmList,23,coordinate_system)
                print("Genou droit")
                angle_dict["RightKnee"] =  angle(lmList,26,coordinate_system)
                print("Genou gauche")                
                angle_dict["LeftKnee"] = angle(lmList,25,coordinate_system)
                #print("Cheville droite")  
                #angle_dict["RightAnkle"] = angle(lmList,28,coordinate_system)
                #print("Cheville gauche")  
                #angle_dict["LeftAnkle"] = angle(lmList,27,coordinate_system)
                #draw_coordinate_system(24,coordinate_system)
                #plot_coordinate_system()
            all_angles[str(frame)] = angle_dict
            #print(new_lmList)
            img = cv2.resize(img, (960, 540)) 


            cv2.imshow('image',img)
           
            frame += 1 
            cv2.waitKey(1)  
        else : 
            process = False

#free the windows
cv2.destroyAllWindows()
video.release()

#writing the result in a text file
with open("output/suiteangletest1.json",'w') as file:
    json.dump(all_angles,file)
    file.close()