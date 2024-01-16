from pytube import YouTube
import tkinter as tk
from tkinter import filedialog

res_stream = None

def download_video(url, save_path):
    try:
        yt = YouTube(url)
        streams = yt.streams.filter(progressive=True, file_extension="mp4")
        res_stream = streams.get_highest_resolution()
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
    root = tk.Tk()
    root.geometry("500x500")
    pic_frame = tk.Frame(root , width=100, height=100, borderwidth=1, relief="groove")
    pic_frame.pack(anchor="center", padx=10, pady=10)
    
    video_url = input("Please enter a YouTube url: ")
    save_dir = open_file_dialog()

    if save_dir:
        print("Started download...")
        download_video(video_url, save_dir)
    else:
        print("Invalid save location.")