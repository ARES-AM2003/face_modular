import cv2

class Camera:
    def __init__(self,height=480,width=640): 
        self.width=width
        self.height=height 
        self.camera=cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH,self.width)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT,self.height)
        self.camera.set(cv2.CAP_PROP_FPS,30)
    

    def get_frame(self):
        while True:
            ret,frame=self.camera.read()
            # ret le chai frame read garyo ki nai check garera t f dinxa 
            if ret:
                cv2.imshow("camera",frame)
                if cv2.waitKey(1) == ord('q'):
                    break
        if ret:
            return frame
        else:
            return None

    def release(self):
        self.camera.release()
