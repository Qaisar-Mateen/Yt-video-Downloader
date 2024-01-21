from os import system
from time import sleep
import requests
import time
import customtkinter as ctk
from pytube import YouTube
from tkinter import filedialog
from PIL import Image


thumbnail_image = None
thumbnail_image_label = None
url = None
but = None
detail_frame = None
pic_frame = None

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

def update_window(title, author, publish_date, thumbnail_url, resulations):
    
    button_mode = "Cancel"
    button_color = "#1F6AA5"
    button_color_hov = "#257EC3"

    thumbnail_image = ctk.CTkImage(Image.open(requests.get(thumbnail_url, stream=True).raw), size=(280, 157))
    thumbnail_image_label.configure(image=thumbnail_image)
    thumbnail_image_label.update()

    detail_frame.destroy()
    detail_frame= ctk.CTkFrame(pic_frame)
    detail_frame.grid(row=0, column=1, pady=25, padx=25, rowspan=1)
    ctk.CTkLabel(detail_frame, text="Title: " + title).grid(row=0, column=0, padx=15, pady=5)
    ctk.CTkLabel(detail_frame, text="Channel: " + author).grid(row=1, column=0, padx=15, pady=5)
    ctk.CTkLabel(detail_frame, text="Publish Date: " + str(publish_date)).grid(row=2, column=0, padx=15, pady=5)
    ctk.CTkLabel(detail_frame, text="Resulation: " + str(resulations)).grid(row=3, column=0, padx=15, pady=5)
    detail_frame.update()

    but.configure(text=button_mode, hover_color=button_color_hov, fg_color=button_color, state="normal")
    but.update()

def fetch_Data(yt_url):
    try:
        start_time = time.time()
        print('fetching...')
        yt = YouTube(yt_url)
        url.configure(state="disabled")
        url.update()
        global resulation, size
        for steam in yt.streams.filter(progressive=True, file_extension="mp4"):
            resulations = steam.resolution
            size = steam.filesize
        
        print("TIME: " + str(time.time()-start_time))

        update_window(yt.title, yt.author, yt.publish_date, yt.thumbnail_url, resulations)
    except Exception as e:
        print(e)
        but.configure(text="Fetch", state="normal")
    
def fetch():
    but.configure(text="Fetching...", state="disabled")
    but.update()
    fetch_Data(url.get())

if __name__ == "__main__":
    
    ctk.set_appearance_mode("dark")

    # root window settings
    root = ctk.CTk()
    root.geometry("900x506")
    root.iconbitmap("icon.ico")
    root.title("YouTube Video Downloader")

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)

    # thumbnail frame
    pic_frame = ctk.CTkFrame(root)
    pic_frame.grid(row=0, column=0, padx=10, pady=(20, 10))
    
    # thumbnail image
    thumbnail_image = ctk.CTkImage(Image.open("no image.png"), size=(280, 157))
    thumbnail_image_label = ctk.CTkLabel(pic_frame, image=thumbnail_image, text="")
    thumbnail_image_label.grid(row=0, column=0, padx=25, pady=25)

    # detail frame
    detail_frame= ctk.CTkFrame(pic_frame)
    detail_frame.grid(row=0, column=1, pady=25, padx=25, rowspan=2)
    ctk.CTkFrame(detail_frame, corner_radius=15, width=189, height=23).grid(row=0, column=0, sticky="w", padx=10, pady=10, columnspan=2)
    ctk.CTkFrame(detail_frame, corner_radius=15, width=120, height=23).grid(row=3, column=0, sticky="w", padx=10, pady=10)
    ctk.CTkFrame(detail_frame, corner_radius=15, width=86, height=23).grid(row=3, column=1, sticky="w", padx=10, pady=10)
    ctk.CTkFrame(detail_frame, corner_radius=15, width=248, height=23).grid(row=2, column=0, sticky="w", padx=10, pady=10, columnspan=2)
    ctk.CTkFrame(detail_frame, corner_radius=15, width=120, height=23).grid(row=1, column=1, sticky="w", padx=10, pady=10)
    ctk.CTkFrame(detail_frame, corner_radius=15, width=86, height=23).grid(row=1, column=0, sticky="w", padx=10, pady=10)
    
    # title frame
    # title_frame = ctk.CTkFrame(pic_frame, corner_radius=10)
    # title_frame.grid(row=1, column=0, pady=(0, 15), padx=15)
    # ctk.CTkLabel(title_frame, text="Title: this is video title").grid(row=0, column=0, padx=15, pady=5)


    # input frame
    input_frame = ctk.CTkFrame(root)
    input_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=(5,30))
    input_frame.grid_columnconfigure((0,1), weight=1)

    url = ctk.CTkEntry(input_frame, placeholder_text="Enter a YouTube URL", width=450)
    url.grid(row=0, column=0, padx=(10, 0), pady=(15, 5), columnspan=1)

    but = ctk.CTkButton(input_frame, text=button_mode, hover_color=button_color_hov, fg_color=button_color, command=fetch)
    but.grid(row=0, column=1, padx=(0, 10), pady=(15, 5))
    

    root.mainloop()

    # video_url = input("Please enter a YouTube url: ")
    # save_dir = open_file_dialog()

    # if save_dir:
    #     print("Started download...")
    #     download_video(video_url, save_dir)
    # else:
    #     print("Invalid save location.")