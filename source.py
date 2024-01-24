import threading
from time import sleep
import requests
import time
import customtkinter as ctk
from pytube import YouTube
from tkinter import CURRENT, filedialog
from PIL import Image


thumbnail_image = None
thumbnail_image_label = None
url = None
but = None
detail_frame = None
pic_frame = None
size_label = None

filesize = []
size_str = "SIZE: - MB"
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

def empty_window():
    global detail_frame, pic_frame, thumbnail_image, thumbnail_image_label

    if(pic_frame):
        pic_frame.destroy()
    if(detail_frame):
        detail_frame.destroy()

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
    # skeleton
    ctk.CTkFrame(detail_frame, corner_radius=15, width=189, height=23).grid(row=0, column=0, sticky="w", padx=10, pady=10, columnspan=2)
    ctk.CTkFrame(detail_frame, corner_radius=15, width=120, height=23).grid(row=3, column=0, sticky="w", padx=10, pady=10)
    ctk.CTkFrame(detail_frame, corner_radius=15, width=86, height=23).grid(row=3, column=1, sticky="w", padx=10, pady=10)
    ctk.CTkFrame(detail_frame, corner_radius=15, width=248, height=23).grid(row=2, column=0, sticky="w", padx=10, pady=10, columnspan=2)
    ctk.CTkFrame(detail_frame, corner_radius=15, width=120, height=23).grid(row=1, column=1, sticky="w", padx=10, pady=10)
    ctk.CTkFrame(detail_frame, corner_radius=15, width=86, height=23).grid(row=1, column=0, sticky="w", padx=10, pady=10)

def update_size(choice):
    global size_str, filesize, avail_resolutions, size_label
    size_str = "SIZE: " + str(filesize[avail_resolutions.index(choice)]) + " MB"
    size_label.configure(text=size_str)
    size_label.update()

def trim_string(s, length):
    if len(s) > length:
        return s[:length] + "..."
    else:
        return s

def update_window(title, author, publish_date, thumbnail_url, avail_resolutions):
    
    button_mode = "Cancel"
    button_color = "#E20000"
    button_color_hov = "red"

    img = Image.open(requests.get(thumbnail_url, stream=True).raw)
    img.thumbnail((280, 157), Image.LANCZOS)
    thumbnail_image = ctk.CTkImage(img)
    thumbnail_image_label.configure(image=thumbnail_image)
    thumbnail_image_label.update()

    global detail_frame, pic_frame, resulation, combobox, size_label
    
    resolution = ctk.IntVar()

    # cleaning frame
    detail_frame.destroy()
    detail_frame= ctk.CTkFrame(pic_frame)
    detail_frame.grid(row=0, column=1, pady=25, padx=25, rowspan=1)
    
    # adding video detail to the frame
    ctk.CTkLabel(detail_frame, text="TITLE: " + trim_string(title, 50)).grid(row=0, column=0, padx=15, pady=5, sticky="w")
    ctk.CTkLabel(detail_frame, text="CHANNEL: " + author).grid(row=1, column=0, padx=15, pady=5, sticky="w")
    ctk.CTkLabel(detail_frame, text="PUBLISH DATE: " + str(publish_date)).grid(row=2, column=0, padx=15, pady=5, sticky="w")
    size_label = ctk.CTkLabel(detail_frame, text = size_str)
    size_label.grid(row=3, column=0, padx=15, pady=5, sticky="w")
    combobox = ctk.CTkComboBox(detail_frame, values=avail_resolutions, command=update_size, variable=resolution)
    combobox.configure(dropdown_hover_color="#257EC3", button_color="#1F6AA5", border_color="#1F6AA5", button_hover_color="#257EC3")
    combobox.grid(row=4, column=0, padx=15, pady=5)
    resolution.set("Select Resolution")
    detail_frame.update()

    but.configure(text=button_mode, hover_color=button_color_hov, fg_color=button_color, state="normal", command=cancel)
    but.update()

def cancel():
    button_mode = "Fetch"
    button_color = "#1F6AA5"
    button_color_hov = "#257EC3"

    but.configure(text=button_mode, hover_color=button_color_hov, fg_color=button_color, state="normal", command=fetch)
    but.update()

    url.configure(state="normal")
    url.update()
    url.delete(0, "end")

    empty_window()

def fetch_Data(yt_url):
    try:
        start_time = time.time()
        print('fetching...')
        yt = YouTube(yt_url)
        url.configure(state="disabled")
        url.update()
        
        global avail_resolutions
        avail_resolutions = []
        for steam in yt.streams.filter(progressive=True, file_extension="mp4"):
            avail_resolutions.append(str(steam.resolution))

            filesize.append(format(steam.filesize / (1024*1024), '.2f'))

        print("TIME: " + str(time.time()-start_time))
        publish_date_str = yt.publish_date.strftime("%d/%m/%Y")
        update_window(yt.title, yt.author, publish_date_str, yt.thumbnail_url, avail_resolutions)

    except Exception as e:
        print(e)
        url.configure(state="normal")
        but.configure(text="Fetch", state="normal")
    
def fetch():
    but.configure(text="Fetching...", state="disabled")
    but.update()
    threading.Thread(target=fetch_Data, args=(url.get(),)).start()
    
if __name__ == "__main__":
    
    ctk.set_appearance_mode("dark")

    # root window settings
    root = ctk.CTk()
    root.geometry("900x506")
    root.iconbitmap("icon.ico")
    root.title("YouTube Video Downloader")

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)

    empty_window()

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