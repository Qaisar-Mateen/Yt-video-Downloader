import threading
import time
import requests
import os
import customtkinter as ctk
from pytube import YouTube, request
from tkinter import filedialog
from PIL import Image


thumbnail_image = None
thumbnail_image_label = None
url = None
but = None
detail_frame = None
pic_frame = None
size_label = None
dir = None
browse_but = None
steam = None
combobox = None
error_label = None
err_frm = None

dir_path = os.path.dirname(os.path.realpath(__file__)) # get current directory path for absolute path
is_paused = False
is_cancelled = False
filesize = []
size_str = "SIZE: - MB"
button_mode = "Fetch"
button_color = "#1A5989"
button_color_hov = "#1F6AA5"

def trim_string(s, length):
    if len(s) > length:
        return s[:length] + "..."
    else:
        return s

def show_error(txt):
    global error_label, err_frm
    err_frm.configure(border_color="#E20000")
    err_frm.update()
    error_label.configure(text=trim_string(txt, 45))
    error_label.update()
    
    time.sleep(3) # to make msg disapear after 3 sec
    err_frm.configure(border_color="#2B2B2B")
    err_frm.update()
    error_label.configure(text="")
    error_label.update()

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
    thumbnail_image = ctk.CTkImage(Image.open(os.path.join(dir_path, "no image.png")), size=(280, 157))
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
    if(float(filesize[avail_resolutions.index(choice)]) >= 1024):
        size_str = "SIZE: " + str(format(float(filesize[avail_resolutions.index(choice)])/(1024), '.2f')) + " GB"
    else:
        size_str = "SIZE: " + str(filesize[avail_resolutions.index(choice)]) + " MB"
    size_label.configure(text=size_str)
    size_label.update()

def update_window(title, author, publish_date, thumbnail_url, avail_resolutions):
    
    button_mode = "Cancel"
    button_color = "#E20000"
    button_color_hov = "red"

    img = Image.open(requests.get(thumbnail_url, stream=True).raw)
    # Calculate the aspect ratio of the image
    aspect_ratio = img.width / img.height
    # Calculate the new size that maintains the aspect ratio
    new_width = 280
    new_height = round(new_width / aspect_ratio)

    # If the calculated height is greater than the upper limit of height, recalculate the width instead
    if new_height > 160:
        new_height = 157
        new_width = round(new_height * aspect_ratio)

    # Resize the image to the new size
    thumbnail_image = ctk.CTkImage(Image.open(requests.get(thumbnail_url, stream=True).raw), size=(new_width, new_height))
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
    size_label = ctk.CTkLabel(detail_frame, text = "SIZE: - MB")
    size_label.grid(row=3, column=0, padx=15, pady=5, sticky="w")
    combobox = ctk.CTkComboBox(detail_frame, values=avail_resolutions, command=update_size, variable=resolution)
    combobox.configure(dropdown_hover_color="#1F6AA5", button_color="#1A5989", border_color="#1A5989", button_hover_color="#1F6AA5")
    combobox.grid(row=4, column=0, padx=15, pady=5)
    resolution.set("Select Resolution")
    detail_frame.update()

    but.configure(text=button_mode, hover_color=button_color_hov, fg_color=button_color, state="normal", command=cancel)
    but.update()

def cancel():
    button_mode = "Fetch"
    button_color = "#1A5989"
    button_color_hov = "#1F6AA5"

    global filesize, avail_resolutions, size_label
    filesize.clear()
    avail_resolutions.clear()
    size_str = "SIZE: - MB"

    but.configure(text=button_mode, hover_color=button_color_hov, fg_color=button_color, state="normal", command=fetch)
    but.update()

    url.configure(state="normal", text_color="#C1E4EE")
    url.update()
    url.delete(0, "end")

    empty_window()

def fetch_Data(yt_url):
    try:
        start_time = time.time()
        print('fetching...')
        yt = YouTube(yt_url)
        url.configure(state="disabled", text_color="#A0B6B6")
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
        if "regex_search: could not find match for" in str(e):
            threading.Thread(target=show_error, args=("ERROR: Invalid URL",)).start()
        elif "getaddrinfo failed" in str(e):
            threading.Thread(target=show_error, args=("ERROR: No Internet Connection",)).start()
        elif "unavailable" in str(e):
            threading.Thread(target=show_error, args=("ERROR: Can't Process this URL",)).start()
        else:
            threading.Thread(target=show_error, args=("ERROR: " + str(e),)).start()
        url.configure(state="normal", text_color="#C1E4EE")
        but.configure(text="Fetch", state="normal")
    
def fetch():
    but.configure(text="Fetching...", state="disabled")
    but.update()
    threading.Thread(target=fetch_Data, args=(url.get(),)).start()

def Browse():
    # Open the directory selection dialog
    directory = filedialog.askdirectory()

    # Set the text of the dir entry to the selected directory
    dir.delete(0, 'end')
    dir.insert(0, directory)

def complete(direc, bar_frm):

    bar_frm.destroy()

    combobox.configure(state="normal")
    global dir, browse_but
    dir = ctk.CTkEntry(input_frame, placeholder_text="Enter Download Directory", width=400)
    dir.insert(0, direc)
    dir.grid(row=3, column=0, padx=(10, 0), pady=(15, 40))
    browse_but = ctk.CTkButton(input_frame, text="Browse...", hover_color="#1F6AA5", fg_color="#1A5989", command=Browse)
    browse_but.grid(row=3, column=1, padx=(0, 10), pady=(15, 40))

    download_but.configure(text="Download", state="normal")
    but.configure(state="normal")

def download_video(url, dir, res, progress, bar, frm):
    try:
        global is_paused, is_cancelled
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension="mp4", resolution=res).first()
        filesize = stream.filesize
        filename = os.path.join(dir, yt.title + ".mp4")
        if filesize < 1024**3:
            progress.configure(text="0%  (0MB/" + f'{filesize / (1024 * 1024):.2f}MB)')
        else:
            progress.configure(text="0%  (0GB/" + f'{filesize / (1024**3):.2f}GB)')
        progress.update()

        with open(filename, 'wb') as f:
            is_paused = is_cancelled = False
            stream = request.stream(stream.url) # get an iterable stream
            downloaded = 0
            while True:
                if is_cancelled:
                    complete(dir,frm)
                    break
                if is_paused:
                    download_but.configure(text="Paused")
                    download_but.update()
                    continue
                
                chunk = next(stream, None) # get next chunk of video
                if chunk:
                    f.write(chunk)  
                    downloaded += len(chunk)
                    str = ''
                    if filesize < 1024**3:
                        str = f'{downloaded / filesize * 100:.1f}%  ({downloaded / (1024 * 1024):.1f}MB/{filesize / (1024 * 1024):.1f}MB)'
                    else:
                        str = f'{downloaded / filesize * 100:.1f}%  ({downloaded / (1024**3):.2f}GB/{filesize / (1024**3):.2f}GB)'
                    
                    bar.set(downloaded / filesize)
                    progress.configure(text=str)
                    progress.update()
        
                else:
                    print('done')
                    complete(dir,frm)
                    break

        if is_cancelled:
            os.remove(filename)

    except Exception as e:
        print(e)

def cncl_download():
    global is_cancelled
    is_cancelled = True
    download_but.configure(text="Canceling...")
    download_but.update()

def action(p_but):
    global is_paused
    is_paused = not is_paused
    p_but.configure(image=ctk.CTkImage(Image.open(os.path.join(dir_path, "play.png")), size=(10, 10)) if is_paused else ctk.CTkImage(Image.open(os.path.join(dir_path, "pause.png")), size=(10, 10)))
    p_but.update()
    if(is_paused):
        download_but.configure(text="Pausing...")
    else:
        download_but.configure(text="Downloading...")
    download_but.update()

def download():
    if combobox == None:
        threading.Thread(target=show_error, args=("ERROR: Fetch Video First",)).start()

    elif combobox.get() == "Select Resolution":
        threading.Thread(target=show_error, args=("ERROR: Select Resolution First",)).start()

    elif dir.get() == "":
        threading.Thread(target=show_error, args=("ERROR: Select Download Directory",)).start()

    else:
        direc = dir.get()
        
        dir.destroy()
        browse_but.destroy()
        combobox.configure(state="disabled")
        combobox.update()
        but.configure(state="disabled")
        but.update()
        download_but.configure(text="Downloading...", state="disabled")
        download_but.update()

        frm = ctk.CTkFrame(input_frame, fg_color="#2B2B2B")
        frm.grid(row=4, column=0, padx=(6, 0), pady=(0, 10), columnspan=2)
        
        lbl = ctk.CTkLabel(frm, text='Location: ' + direc, font=("Arial", 12))
        lbl.grid(row=0, column=0, padx=(10, 0), pady=(10,4), sticky="w")

        bar = ctk.CTkProgressBar(frm, fg_color="#242424", progress_color="#1A5989", width=400, height=18)
        bar.grid(row=1, column=0, padx=(10,5), pady=(1, 5))
        bar.set(0)

        progress = ctk.CTkLabel(frm, text='0% (0MB/0MB)')
        progress.grid(row=1, column=1, padx=2, pady=(1, 5), columnspan=1, sticky = "w")

        fr = ctk.CTkFrame(frm, fg_color="#2B2B2B")
        fr.grid(row=1, column=3, padx= 0, pady=0)
        fr.columnconfigure((0,1), weight=1)

        ic_path = os.path.join(dir_path, "cancel.png")
        img = ctk.CTkImage(Image.open(ic_path), size=(10, 10))
        cancel_but = ctk.CTkButton(fr, image=img, text='', command=cncl_download, hover_color="#1F6AA5", fg_color="#1A5989", width=20, height=20)
        cancel_but.grid(row=0, column=1, padx=10, pady=(1, 5), columnspan=1)

        ia_path = os.path.join(dir_path, "pause.png") 
        img = ctk.CTkImage(Image.open(ia_path), size=(10, 10))
        p_but = ctk.CTkButton(fr, image=img, text='', hover_color="#1F6AA5", command=lambda: action(p_but), fg_color="#1A5989", width=20, height=20)
        p_but.grid(row=0, column=0, padx=10, pady=(1, 5), columnspan=1)

        print("Started download...")
        threading.Thread(target=download_video, args=(url.get(), direc, combobox.get(), progress, bar, frm)).start()

if __name__ == "__main__":
    
    ctk.set_appearance_mode("dark")

    # root window settings
    root = ctk.CTk()
    root.geometry("930x540")
    root.resizable(False, False)
    icon_path = os.path.join(dir_path, "icon.ico")
    root.iconbitmap(icon_path)
    root.title("YouTube Video Downloader")

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)

    empty_window()

    # input frame
    input_frame = ctk.CTkFrame(root)
    input_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=(5,30))
    input_frame.grid_columnconfigure((0,1), weight=1)

    err_frm = ctk.CTkFrame(input_frame, fg_color="#2B2B2B", border_width=1, border_color="#2B2B2B")
    err_frm.grid(row=0, column=0, padx=(0), pady=(15, 0), columnspan=2)
    error_label = ctk.CTkLabel(err_frm, text="", text_color="#E20000")
    error_label.grid(row=0, column=0, padx=(10), pady=(5))    

    url = ctk.CTkEntry(input_frame, placeholder_text="Enter a YouTube URL", width=400, )
    url.grid(row=1, column=0, padx=(10, 0), pady=(15, 5), columnspan=1)
    but = ctk.CTkButton(input_frame, text=button_mode, hover_color=button_color_hov, fg_color=button_color, command=fetch)
    but.grid(row=1, column=1, padx=(0, 10), pady=(5, 5), columnspan=1)
    
    dir = ctk.CTkEntry(input_frame, placeholder_text="Enter Download Directory", width=400)
    dir.grid(row=3, column=0, padx=(10, 0), pady=(15, 25))
    browse_but = ctk.CTkButton(input_frame, text="Browse...", hover_color="#1F6AA5", fg_color="#1A5989", command=Browse)
    browse_but.grid(row=3, column=1, padx=(0, 10), pady=(15, 25))

    download_but = ctk.CTkButton(input_frame, text="Download", hover_color="#1F6AA5", fg_color="#1A5989", width=200, command=download)
    download_but.grid(row=5, column=0, padx=(10, 0), pady=(5, 15), columnspan=2)

    root.mainloop()