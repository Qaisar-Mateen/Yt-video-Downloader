from time import sleep
import customtkinter as ctk
import urllib.request
from pytube import YouTube
from tkinter import filedialog
from PIL import Image
from io import BytesIO

thumbnail_image = None
thumbnail_image_label = None
url = None
but = None

button_mode = "Fetch"
button_color = "#1F6AA5"
button_color_hov = "#257EC3"

# def download_video(url, save_path):
#     try:
#         yt = YouTube(url)
#         streams = yt.streams.filter(progressive=True, file_extension="mp4")
#         res_stream = streams.get_highest_resolution()
        
#         if res_stream:
#             res_stream.download(output_path=save_path)

#         print("Video downloaded successfully!")
#     except Exception as e:
#         print(e)

def open_file_dialog():
    folder = filedialog.askdirectory()
    if folder:
        print(f"Selected folder: {folder}")

    return folder

def fetch_Data(yt_url):
    try:
        print("Fetching data...")
        yt = YouTube(yt_url)
        url.configure(state="disabled")

        global resulations, title, channel, pub_date, img_url
    
        for steam in yt.streams.filter(progressive=True, file_extension="mp4"):
            resulations = steam.resolution
            
        channel = yt.author
        pub_date = yt.publish_date
        img_url = yt.thumbnail_url
        title = yt.title

    except Exception as e:
        print(e)

def wrapper_fetch_Data(yt_url):
    but.configure(text="Fetching...")
    sleep(1)
    fetch_Data(yt_url)
    but.configure(text=button_mode)

if __name__ == "__main__":
    
    ctk.set_appearance_mode("dark")

    # root window settings
    root = ctk.CTk()
    root.geometry("900x506")
    root.resizable(False, False)
    root.iconbitmap("icon.ico")
    root.title("YouTube Video Downloader")

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)

    # thumbnail frame
    pic_frame = ctk.CTkFrame(root)
    pic_frame.grid(row=0, column=0, padx=10, pady=(20, 10))
    pic_frame.grid_rowconfigure(0, weight=1)
    # thumbnail image
    thumbnail_image = ctk.CTkImage(Image.open("no image.png"), size=(280, 157))
    thumbnail_image_label = ctk.CTkLabel(pic_frame, image=thumbnail_image, text="")
    thumbnail_image_label.grid(row=0, column=0, padx=25, pady=25)

    detail_frame= ctk.CTkFrame(pic_frame)
    detail_frame.grid(row=0, column=1)
    
    title_frame = ctk.CTkFrame(pic_frame)
    title_frame.grid(row=1, column=0, pady=(0, 15), padx=15)
    ctk.CTkLabel(title_frame, text="Title: this is video title", corner_radius=15).grid(row=0, column=0, padx=5, pady=5)
    # input frame
    input_frame = ctk.CTkFrame(root)
    input_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=(5,30))
    input_frame.grid_columnconfigure((0,1), weight=1)

    url = ctk.CTkEntry(input_frame, placeholder_text="Enter a YouTube URL", width=450)
    url.grid(row=0, column=0, padx=(10, 0), pady=(15, 5), columnspan=1)

    but = ctk.CTkButton(input_frame, text=button_mode, hover_color=button_color_hov, fg_color=button_color, command=lambda: wrapper_fetch_Data(url.get()))
    but.grid(row=0, column=1, padx=(0, 10), pady=(15, 5))



    root.mainloop()

    # video_url = input("Please enter a YouTube url: ")
    # save_dir = open_file_dialog()

    # if save_dir:
    #     print("Started download...")
    #     download_video(video_url, save_dir)
    # else:
    #     print("Invalid save location.")