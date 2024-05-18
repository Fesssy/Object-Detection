import tkinter as tk
import cv2
from PIL import Image, ImageTk
from tkinter import filedialog

path = None

def run_camera_app():
    # Global variables
    cap = None  # Webcam capture object
    camera_label = None  # Label for displaying camera feed
    captured_image = None  # Variable to store the captured image

    # Function to start the camera
    def start_camera():
        nonlocal cap
        cap = cv2.VideoCapture(0)  # Initialize the webcam (adjust camera index as needed)
        
        if not cap.isOpened():
            print("Error: Could not open camera.")
            return
        
        # Function to update the camera feed on the GUI
        def update_camera_feed():
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                camera_label.config(image=photo)
                camera_label.photo = photo
                camera_label.after(10, update_camera_feed)  # Update the feed every 10 milliseconds
            else:
                cap.release()
                camera_label.config(image="")

        update_camera_feed()

    # Function to capture an image
    def capture_image():
        nonlocal captured_image
        ret, frame = cap.read()
        if ret:
            captured_image = frame
            print("Image captured.")
        else:
            print("Error: Could not capture image.")

    # Function to save the captured image
    def save_image():
        global path
        nonlocal captured_image
        if captured_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
            if file_path:
                path = file_path
                cv2.imwrite(file_path, captured_image)
                print(f"Image saved as {file_path}")
        else:
            print("Error: No image to save.")

    # Create the main application window
    root = tk.Tk()
    root.title("Camera App")

    # Create a button to start the camera
    start_button = tk.Button(root, text="Start Camera", command=start_camera)
    start_button.pack(pady=10)

    # Create a button to capture an image
    capture_button = tk.Button(root, text="Capture Image", command=capture_image)
    capture_button.pack(pady=10)

    # Create a button to save the captured image
    save_button = tk.Button(root, text="Save Image", command=save_image)
    save_button.pack(pady=10)

    # Create a label to display the camera feed
    camera_label = tk.Label(root)
    camera_label.pack()

    # Run the GUI application
    root.mainloop()

if __name__ == "__main__":
    run_camera_app()
