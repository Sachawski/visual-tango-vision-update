import cv2
import mediapipe as mp
import numpy as np
import math
import json
from scipy.spatial.transform import Rotation

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

process = True

#Processing of the video 
with mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as pose:
    #import the video to process
    try:
        video = cv2.VideoCapture('IMG_5395.MOV')
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
            
        
            # render detection
            mp_drawing.draw_landmarks(img,results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245,117,66),thickness=2,circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245,66,230),thickness=2,circle_radius=2))


            # 11,12,13,14,15,16,23-28
            
            img = cv2.resize(img, (960, 540)) 
            cv2.imshow('image',img)
           
            frame += 1 
            cv2.waitKey(1)  

            with open("AnimationFile.txt","w") as f:
                f.writelines(["%s\n" % item for item in posList])

        else : 
            process = False

#free the windows
cv2.destroyAllWindows()
video.release()
