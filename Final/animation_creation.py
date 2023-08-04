import cv2
import mediapipe as mp
import numpy as np
import math
import json
from scipy.spatial.transform import Rotation

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


def sachaleboss(atraiter):
    print("sacha")
    print(atraiter)
    process = True
    #Processing of the video 
    with mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as pose:
        #import the video to process
        try:
            video = cv2.VideoCapture(atraiter)
        except:
            print('pas de video')
        n = 33
        frame = 0
        posList = []
        while process:

            success,img = video.read()
            if success:
                print(frame)
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
                        lmList[i,0] = landmarks[i].x
                        lmList[i,1] = landmarks[i].y
                        lmList[i,2] = landmarks[i].z
                except : 
                    pass
            
                try :
                    lmString = ''
                    for lm in lmList:
                        
                        lmString += f'{lm[0]},{(1-lm[1])},{lm[2]},'

                    posList.append(lmString)
                except:
                    pass
            

                # 11,12,13,14,15,16,23-28
                
                frame += 1

            else : 
                process = False

    #free the windows
    print(posList)
    video.release()
    return posList