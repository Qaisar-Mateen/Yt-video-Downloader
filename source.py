from pytube import YouTube
#import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from PIL import ImageTk, Image

res_stream = None

def download_video(url, save_path):
    try:
        yt = YouTube(url)
        streams = yt.streams.filter(progressive=True, file_extension="mp4")
        res_stream = streams.get_highest_resolution()
        
        if res_stream:
            res_stream.download(output_path=save_path)

        print("Video downloaded successfully!")
    except Exception as e:
        print(e)

def open_file_dialog():
    folder = filedialog.askdirectory()
    if folder:
        print(f"Selected folder: {folder}")

    return folder

if __name__ == "__main__":
    
    ctk.set_appearance_mode("dark")

    # root window settings
    root = ctk.CTk()
    root.geometry("890x501")
    root.title("YouTube Video Downloader")

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    # frame = ctk.CTkFrame(root)
    # frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    # thumbnail frame
    pic_frame = ctk.CTkFrame(root, width=260, height=151)
    pic_frame.grid(row=0, column=0, padx=10, pady=(20, 10))

    # thumbnail image
    thumbnail_image = ctk.CTkImage(Image.open("no image.png"), size=(250, 141))
    thumbnail_image_label = ctk.CTkLabel(pic_frame, image=thumbnail_image, text="")
    thumbnail_image_label.grid(row=0, column=0, padx=25, pady=25)

    # input frame
    input_frame = ctk.CTkFrame(root)
    input_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=(5,30))

    # input_frame = tk.Frame(frame)
    # input_frame.pack(anchor="center", fill=tk.X ,padx=10, pady=10)
    # urlbox = tk.Entry(input_frame, width=50, borderwidth=2, relief="groove")
    # urlbox.pack(anchor="center", padx=10, pady=10)

    but = ctk.CTkButton(input_frame, fg_color="#FF0000", hover_color="#333333")#, active_color="#4d4d4d", width=20, height=2, borderwidth=0)
    but.grid(row=0, column=0, sticky="s", padx=40, pady=40)

    root.mainloop()

    # video_url = input("Please enter a YouTube url: ")
    # save_dir = open_file_dialog()

    # if save_dir:
    #     print("Started download...")
    #     download_video(video_url, save_dir)
    # else:
    #     print("Invalid save location.")