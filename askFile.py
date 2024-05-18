import tkinter as tk
from tkinter import filedialog

path = None
name = None

def main(a):
    global name
    def open_file_dialog():
        global path
        if 1==a:
            name = "Video"
            file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi *.mkv")])
        elif 0==a:
            name = "Image"
            file_path = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpg")])
        if file_path:
            entry_var.set(file_path)
            path = file_path

    # Create a basic tkinter window
    root = tk.Tk()
    root.title("File Location")

    # Create a label and entry field to display the selected file path
    label = tk.Label(root, text="File Location:")
    label.pack()

    entry_var = tk.StringVar()
    entry = tk.Entry(root, textvariable=entry_var, width=40)
    entry.pack()

    # Create a "Browse" button to open a file dialog
    browse_button = tk.Button(root, text="Browse", command=open_file_dialog)
    browse_button.pack()

    # Create a "Submit" button to perform actions with the selected file location
    def perform_action():
        file_location = entry_var.get()
        # You can add your code here to work with the selected file location
        if file_location:
            print("Performing action with file:", file_location)

    submit_button = tk.Button(root, text="Open", command=perform_action)
    submit_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
