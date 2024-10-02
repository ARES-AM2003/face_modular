import face_recognition
import threading
import queue
import cv2

class face_handler:
    def __init__(self, reference_img_path):
        # Load reference image and initialize queue/thread
        self.width = 640
        self.height = 480
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.camera.set(cv2.CAP_PROP_FPS, 30)
        self.reference_img = face_recognition.load_image_file(reference_img_path)
        self.reference_encoding = face_recognition.face_encodings(self.reference_img)[0]
        self.face_match = False
        self.frame_queue = queue.Queue()
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.check_face)
        self.thread.start()

    def check_face(self):
        while not self.stop_event.is_set():
            frame = self.frame_queue.get()
            if frame is None:
                continue
            
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)
            self.face_match = any(face_recognition.compare_faces([self.reference_encoding], encoding) for encoding in face_encodings)

    def validate_face(self):
        cnt = 0
        while True:
            ret, frame = self.camera.read()
            if not ret:
                break

            if cnt % 10 == 0:
                self.frame_queue.put(frame.copy())

            if cnt>70:
                break
            
            if self.face_match:
                cv2.putText(frame, "Face Match", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                break

            cv2.imshow("Camera", frame)

            # Break on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            cnt += 1

        self.clean_up()

        return self.face_match

    def clean_up(self):
        # Stop the thread and release resources
        self.frame_queue.put(None)
        self.stop_event.set()
        if self.thread.is_alive():
            self.thread.join()
        self.camera.release()
        cv2.destroyAllWindows()
