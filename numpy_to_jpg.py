import numpy as np
import cv2

# Load the 1D .npy file
npy_file_path = '/home/aresam/Desktop/face_mofular/images/rochak.jpg.npy'
image_data = np.load(npy_file_path)

# You need to know the original dimensions (e.g., 100x100 pixels)
height = 16
width = 8

# Reshape the 1D array to 2D (for grayscale)
image_data = image_data.reshape((height, width))

# If the values are not in 0-255 range, normalize them
if image_data.max() > 255 or image_data.min() < 0:
    image_data = (image_data - image_data.min()) / (image_data.max() - image_data.min())  # Normalize to 0.0 - 1.0
    image_data = (image_data * 255).astype(np.uint8)  # Convert to 0-255 range

# Save the reshaped array as a .jpg image
output_jpg_path = '/home/aresam/Desktop/face_mofular/images/rochak12.jpg'
cv2.imwrite(output_jpg_path, image_data)

print(f"Grayscale image saved as {output_jpg_path}")
