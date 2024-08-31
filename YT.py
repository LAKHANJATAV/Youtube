import streamlit as st
import yt_dlp
import os

# Streamlit App
st.title("YouTube Video Downloader")

# Input for YouTube URL
url = st.text_input("Enter the YouTube Video URL:")

best_video_format = None
best_audio_format = None

if url:
    try:
        ydl_opts = {
            'quiet': True,
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4'
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            formats = info_dict.get('formats', None)
            video_title = info_dict.get('title', 'video')

        # Find the best video and audio formats
        best_video_format = next((f for f in formats if f.get('vcodec') != 'none' and f.get('acodec') == 'none'), None)
        best_audio_format = next((f for f in formats if f.get('acodec') != 'none' and f.get('vcodec') == 'none'), None)

        if best_video_format and best_audio_format:
            st.write(f"**Selected Quality:** {best_video_format.get('resolution', 'Unknown')} (Video) + Audio")
        else:
            st.error("No suitable video or audio format found")

    except yt_dlp.utils.DownloadError as e:
        st.error(f"An error occurred while fetching video details: {e}")
        best_video_format = None
        best_audio_format = None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        best_video_format = None
        best_audio_format = None

# Default save location to C:\Users\<Username>\Downloads
default_save_location = os.path.join(os.path.expanduser("~"), "Downloads")
save_location = st.text_input("Enter the Save Location Path:", value=default_save_location)

# Download button and logic
if st.button("Download"):
    if url:
        try:
            video_file_name = f"{video_title}.mp4"
            temp_file_path = os.path.join(save_location, video_file_name)

            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',  # Always download the best available quality
                'merge_output_format': 'mp4',  # Ensure the output is in MP4 format
                'outtmpl': temp_file_path,
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4'}]  # Convert to mp4 if necessary
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            st.success("Download Complete!")

            with open(temp_file_path, "rb") as file:
                st.download_button(
                    label="Download Video",
                    data=file,
                    file_name=video_file_name,
                    mime="video/mp4"
                )

        except yt_dlp.utils.DownloadError as e:
            st.error(f"Download failed: {str(e)}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
    else:
        st.error("Please enter a YouTube URL.")
