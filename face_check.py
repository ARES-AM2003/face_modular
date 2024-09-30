import face_recognition
import threading
import queue

class face_handler:
    def __init__(self,reference_img_path):
        # regrence image line ani load garni sangai que initilize garni ani thread chalai dine
        self.reference_img_path=reference_img_path
        self.reference_img=face_recognition.load_image_file(self.reference_img_path)
        self.reference_encoding=face_recognition.face_encodings(self.reference_img)[0]
        self.face_match=False
        self.frame_queue=queue.Queue()
        self.thread=threading.Thread(target=self.check_face)
        self.thread.start()
    
    def check_face(self):
        while True:
            frame=self.frame_queue.get()
            if frame is None:
                break
            face_locations=face_recognition.face_locations(frame)
            face_encodings=face_recognition.face_encodings(frame,face_locations)
            self.face_match=False
            for face_encoding in face_encodings:
                matches=face_recognition.compare_faces([self.reference_encoding],face_encoding)
                if True in matches:
                    self.face_match=True
                    break

    def add_frame(self,frame):
        self.frame_queue.put(frame)



    def release(self):
        self.frame_queue.put(None)
        self.thread.join()
