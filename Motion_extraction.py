import cv2
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from threading import Thread


def select_video():
    filepath = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
    if filepath:
        entry_video.delete(0, tk.END)
        entry_video.insert(0, filepath)


def convert_video():
    input_path = entry_video.get()
    if not input_path:
        messagebox.showerror("Error", "Please select a video file.")
        return

    output_path = input_path[:-4] + "_motion_extraction.mp4"  # Change the file extension to .mp4

    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps,
                          (frame_width, frame_height))  # Use MP4V codec for MP4 format

    success, prev_frame = cap.read()
    if not success:
        messagebox.showerror("Error", "Failed to read video.")
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    progress_bar.config(maximum=total_frames)

    while True:
        success, curr_frame = cap.read()
        if not success:
            break

        diff = cv2.absdiff(curr_frame, prev_frame)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        _, motion_mask = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)

        out.write(cv2.cvtColor(motion_mask, cv2.COLOR_GRAY2BGR))

        progress_bar.step(1)
        root.update_idletasks()

        prev_frame = curr_frame

    out.release()
    cap.release()

    messagebox.showinfo("Success", "Motion extraction completed.")


def download_video():
    output_path = entry_video.get()[:-4] + "_motion_extraction.mp4"
    if not output_path:
        messagebox.showerror("Error", "No motion extraction video found.")
        return

    filedialog.asksaveasfilename(initialfile=output_path.split("/")[-1], defaultextension=".mp4")


root = tk.Tk()
root.title("Motion Extraction")
root.geometry("400x200")

label_video = tk.Label(root, text="Video File:")
label_video.pack()

entry_video = tk.Entry(root, width=40)
entry_video.pack()

button_upload = tk.Button(root, text="Upload Video", command=select_video)
button_upload.pack()

button_convert = tk.Button(root, text="Convert Video", command=convert_video)
button_convert.pack()

progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=300, mode="determinate")
progress_bar.pack()

button_download = tk.Button(root, text="Download Motion Extraction Video", command=download_video)
button_download.pack()

root.mainloop()
