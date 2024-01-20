from pytube import YouTube
#import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from PIL import ImageTk, Image

res_stream = None
button_mode = "Download"
button_color = "#1F6AA5"
button_color_hov = "#257EC3"

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
    root.geometry("900x506")
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
    thumbnail_image_label = ctk.CTkLabel(pic_frame, image=thumbnail_image, text="", width=260, height=151)
    # thumbnail_image_label.configure(bg_color="#1F1F1F",corner_radius=15)
    thumbnail_image_label.grid(row=0, column=0, padx=25, pady=25)

    # input frame
    input_frame = ctk.CTkFrame(root)
    input_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=(5,30))
    input_frame.grid_columnconfigure((0,1), weight=1)

    url = ctk.CTkEntry(input_frame, placeholder_text="Enter a YouTube URL", width=450)
    url.grid(row=0, column=0, padx=(10, 0), pady=(15, 5), columnspan=1)

    but = ctk.CTkButton(input_frame, text=button_mode, hover_color=button_color_hov, fg_color=button_color)
    but.grid(row=0, column=1, sticky="", padx=(0, 10), pady=(15, 5))

    root.mainloop()

    # video_url = input("Please enter a YouTube url: ")
    # save_dir = open_file_dialog()

    # if save_dir:
    #     print("Started download...")
    #     download_video(video_url, save_dir)
    # else:
    #     print("Invalid save location.")