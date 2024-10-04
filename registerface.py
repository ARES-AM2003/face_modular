import os
import cv2
import face_recognition

class Register_Face:
    def __init__(self, name):
        self.name = name
        self.width = 640
        self.height = 480
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.camera.set(cv2.CAP_PROP_FPS, 30)
        self.frame_count = 0
        self.image_path = os.path.join("images", self.name+ '.jpg')
        self.save_image = False  # Flag to control when to save image


    # takes event x y flag param in mouse event in cv2 mouse callback function
    def capture_frame(self, event, x, y, flags, param):
        """Callback function to capture frame on mouse left button click."""
        if event == cv2.EVENT_LBUTTONDOWN:
            self.save_image = True

    def Register(self):
        # Set up the mouse callback function to capture frames on click
        cv2.namedWindow("Camera")
        cv2.setMouseCallback("Camera", self.capture_frame)

        while True:
            ret, frame = self.camera.read()
            if not ret:
                print("Failed to capture image")
                break

            # Display the camera feed
            cv2.imshow("Camera", frame)

            if self.save_image:
                # Save the image on click
                face_locations = face_recognition.face_locations(frame)
                if face_locations:
                    
                    print(f"Saving image: {self.image_path}")
                    cv2.imwrite(self.image_path, frame)
                
                    break
                print("No face detected in the frame.")
                self.save_image = False
            # Press 'q' to quit the camera loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the camera and close windows
        self.camera.release()
        cv2.destroyAllWindows()

