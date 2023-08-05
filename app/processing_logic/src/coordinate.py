from scipy.spatial.transform import Rotation
import numpy as np

POSE_ARTICULATIONS = {
    14:(12,14,16), 13:(11,13,15), 24:(12,24,26), 23:(11,23,25), 26:(24,26,28), 25:(23,25,27),
    28:(26,28,32), 27:(25,27,31)
}

COORDINATE_SYSTEM_INIT_DICT = {
    24:(12,24,23), 23:(11,23,24)
} 

ARTICULATIONS = set([13,14,24,23,26,25,28,27])

def coordinate_system_initialisation(lmList,articulation):

    if articulation == 24 or articulation == 23 :
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
        
    return O,OX,OY,OZ,P     




def coordinate_system_update(lmList,articulation,coordinate_system):

    p1 = POSE_ARTICULATIONS[articulation][0]
    p2 = POSE_ARTICULATIONS[articulation][1]
    p3 = POSE_ARTICULATIONS[articulation][2]
    
    new_O = np.array([lmList[p2,0],lmList[p2,1],lmList[p2,2]])
    OX = coordinate_system[articulation][1] - new_O
    OY = coordinate_system[articulation][2] - new_O
    OZ = coordinate_system[articulation][3] - new_O

    new_OY_to_align = np.array([[lmList[p1,0],lmList[p1,1],lmList[p1,2]]]) - new_O

    #rota,_ = Rotation.align_vectors(new_OY_to_align,[OY])
   
    new_OX = rota.apply(OX)
    new_OY = rota.apply(OY)
    new_OZ = rota.apply(OZ)
    new_P = np.array([[new_OX[0],new_OY[0],new_OZ[0]],
                      [new_OX[1],new_OY[1],new_OZ[1]],
                      [new_OX[2],new_OY[2],new_OZ[2]]])

    return new_O,new_OX,new_OY,new_OZ,new_P  
    