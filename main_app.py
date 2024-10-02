import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk  # CustomTkinter for buttons
from registerface import Register_face
from face_check import face_handler
import os
import threading

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Face Recognition App")
        self.geometry("1000x800")

        # Configure 1x2 layout for the entire app
        self.rowconfigure(0, weight=1)  # Only one row
        self.columnconfigure(0, weight=2, minsize=500)  # First column (image)
        self.columnconfigure(1, weight=1, minsize=500)  # Second column (content)

        # Load and display the image in the first column
        self.load_image()

        # Create a frame for the content (buttons and navigation) in the second column
        self.content_frame = tk.Frame(self)
        self.content_frame.grid(row=0, column=1, sticky="nsew")

        # Initialize pages and frame management
        self.frames = {}
        for F in (HomePage, Verify, Register):
            frame = F(self.content_frame, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the home page initially
        self.show_frame(HomePage)

    def load_image(self):
        """Load and display the image in the first column."""
        try:
            img = Image.open("images/img.jpg")
            img = img.resize((500, 800), Image.LANCZOS)  # Resize to fit the left column
            img_tk = ImageTk.PhotoImage(img)

            # Create a label to display the image
            img_label = tk.Label(self, image=img_tk, bg="black")
            img_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

            # Keep a reference to the image to prevent garbage collection
            img_label.image = img_tk

        except FileNotFoundError:
            img_label = tk.Label(self, text="Image not found", bg="black")
            img_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    def show_frame(self, cont):
        """Show a frame for the given page."""
        frame = self.frames[cont]
        frame.tkraise()  # Raise the frame to the top of the stack


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Create buttons for navigating to other pages
        self.create_navigation_buttons(controller)

    def create_navigation_buttons(self, controller):
        """Create buttons for Register and Verify actions using CustomTkinter."""
        register_button = ctk.CTkButton(self, text="Register Face", command=lambda: controller.show_frame(Register))
        register_button.pack(pady=20, padx=10, fill="x")

        verify_button = ctk.CTkButton(self, text="Verify Face", command=lambda: controller.show_frame(Verify))
        verify_button.pack(pady=10, padx=10, fill="x")


class Verify(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        label = tk.Label(self, text="Proceed to verify", font=("Helvetica", 18))
        label.pack(pady=10, padx=10)

        # Input label and entry box
        input_label = tk.Label(self, text="Enter your name:")
        input_label.pack(pady=5)
        self.input_entry = tk.Entry(self)  # Store as an instance variable to access later
        self.input_entry.pack(pady=5)

        # Result label to display success or error messages
        self.result_label = None

        def verify_face():
            """Retrieve the input and call face verification."""
            name = self.input_entry.get()  # Get the input from the entry box
            image_path = os.path.join("images", name + ".jpg")
            print(f"Verifying {name} with image path: {image_path}")

            # Call the face_handler function to verify the face
            if self.result_label:  # Clear previous result label if it exists
                self.result_label.destroy()

            try:
                face=face_handler(image_path)
                x=face.validate_face()
                
                print(x)
                self.result_label = ctk.CTkLabel(self, text='', font=("Helvetica", 18))
                self.result_label.pack(pady=10, padx=10)
                
                
                if x:
                    self.result_label = ctk.CTkLabel(self, text="Face Verified", font=("Helvetica", 18), fg_color="green")
                    self.result_label.pack(pady=10, padx=10)
                else:
                    self.result_label = ctk.CTkLabel(self, text='Not verified', font=("Helvetica", 18), fg_color="red")
                    self.result_label.pack(pady=10, padx=10)
            except Exception as e:
                print(e)
                self.result_label = ctk.CTkLabel(self, text='Face not registered', font=("Helvetica", 18), fg_color="red")
                self.result_label.pack(pady=10, padx=10)

        # Create a button to trigger the face verification
        verify_button = ctk.CTkButton(self, text="Verify Face", command=verify_face)
        verify_button.pack(pady=10, padx=10)

        back_button = ctk.CTkButton(self, text="Back to Home", command=lambda: controller.show_frame(HomePage))
        back_button.pack(pady=5)


class Register(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        label = tk.Label(self, text="This is the Register Page", font=("Helvetica", 18))
        label.pack(pady=10, padx=10)

        back_button = ctk.CTkButton(self, text="Back to Home", command=lambda: controller.show_frame(HomePage))
        back_button.pack(pady=5)


# Run the application
if __name__ == "__main__":
    app = Application()
    app.mainloop()
