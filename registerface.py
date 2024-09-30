import camera
import os
import numpy as np
import cv2
import face_recognition

class Register_face:
    def __init__(self,name):
        self.name=name
        self.camera=camera.Camera()
        self.frame_count=0
        self.image_path=os.path.join("images",self.name+".jpg")
       
        

    def Register(self):
        while True:
            frame = self.camera.get_frame()
            if frame is None:
                break

            
            cv2.imwrite(self.image_path, frame)
            self.frame_count += 1
            if self.frame_count >= 5:
                break
            
            

        cv2.destroyAllWindows()
    
   


