import customtkinter as ctk
import os
from tkinter import ttk
from tkinter import filedialog
from pytube import YouTube

def dl_video():
    url = entry_url.get()
    f_type = filetype_var.get()

    status_label.pack(pady=(10,5))
    progress_label.pack(pady=(10,5))
    progress_bar.pack(pady=(10,5))
    
    # Hide and reset the progress bar and percentage label when download button is pressed again
    progress_label.configure(text="0%")
    progress_bar.set(0)
    status_label.configure(text="")

    try:
        yt = YouTube(url)
        yt.register_on_progress_callback(on_progress)  # Register the progress callback

        # Let the user choose the save location and file name

        if f_type == "MP4":
            download_path = filedialog.asksaveasfilename(
            defaultextension='mp4',
            filetypes=[("MP4 Video", "*.mp4")],
            )
            if not download_path:
                status_label.configure(text="Download cancelled.", text_color="white", fg_color="red")
                return
            directory, filename = os.path.split(download_path)
            base_filename, ext = os.path.splitext(filename)
            video_stream = yt.streams.get_highest_resolution().download(output_path=directory, filename=base_filename)
            os.rename(video_stream, download_path)
            status_label.configure(text=f"Successfully Downloaded {yt.title}", text_color="white", fg_color="green")
        
        elif f_type == "MP3":
            download_path = filedialog.asksaveasfilename(
            defaultextension='mp3',
            filetypes=[("MP3 Audio", "*.mp3")],
            )
            if not download_path:
                status_label.configure(text="Download cancelled.", text_color="white", fg_color="red")
                return
            directory, filename = os.path.split(download_path)
            base_filename, ext = os.path.splitext(filename)
            audio_stream = yt.streams.get_audio_only().download(output_path=directory, filename=base_filename)
            os.rename(audio_stream, download_path)
            if not download_path:
                status_label.configure(text="Download cancelled.", text_color="white", fg_color="red")
                return
            status_label.configure(text=f"Successfully Downloaded {yt.title}", text_color="white", fg_color="green")

    except Exception as e:
        status_label.configure(text=f"Error: {str(e)}", text_color="white", fg_color="red")
        print(e)

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_completed = bytes_downloaded / total_size * 100
    progress_label.configure(text=str(int(percentage_completed)) + "%")
    progress_label.update()
    
    progress_bar.set(float(percentage_completed / 100))

# System settings
app = ctk.CTk()
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

# App title
app.title("Youtube Downloader")

# set min and max width and height
app.geometry("720x480")
app.minsize(720, 480)
app.maxsize(1080, 720)

# create frame to hold content
app_frame = ctk.CTkFrame(app)
app_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

# create a label and the entry widget for the url
url_label = ctk.CTkLabel(app_frame, text="Enter the youtube url here: ")
entry_url = ctk.CTkEntry(app_frame, width=400, height=40)
url_label.pack(pady=(10,5))
entry_url.pack(pady=(10,5))

# create a file type combo box
filetype = ["MP3", "MP4"]
filetype_var = ctk.StringVar()
filetype_label = ctk.CTkLabel(app_frame, text="Choose File Type")
filetype_label.pack(pady=(10,5))
filetype_combobox = ttk.Combobox(app_frame, values=filetype, textvariable=filetype_var)
filetype_combobox.pack(pady=(10,5))
filetype_combobox.set("Select File Type")

# create a download button
dl_button = ctk.CTkButton(app_frame, text="Download", command=dl_video)
dl_button.pack(pady=(10,5))

# create a label and progress bar to display download progress
progress_label = ctk.CTkLabel(app_frame, text="0%")
progress_bar = ctk.CTkProgressBar(app_frame, width=400)
progress_bar.set(0)

# create status level
status_label = ctk.CTkLabel(app_frame, text="")

# Run app
app.mainloop()