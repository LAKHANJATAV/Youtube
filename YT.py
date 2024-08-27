import streamlit as st
import yt_dlp
import os

# Streamlit App
st.title("YouTube Video Downloader")

# Input for YouTube URL
url = st.text_input("Enter the YouTube Video URL:")

best_single_format = None  # Initialize best_single_format before the try block

if url:
    try:
        # Fetch video information
        ydl_opts = {'quiet': True, 'format': 'best'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            formats = info_dict.get('formats', None)

        # Filter for best single format (video + audio)
        best_single_format = next((f for f in formats if f.get('acodec') != 'none' and f.get('vcodec') != 'none'), None)
        if best_single_format:
            option_str = f"{best_single_format['format_id']} - {best_single_format.get('resolution', 'Unknown')} - {best_single_format['ext']}"
            st.write(f"**Selected Quality:** {option_str}")
        else:
            st.error("No suitable format found")
            best_single_format = None  # Set to None if no format is found

    except yt_dlp.utils.DownloadError as e:
        st.error(f"An error occurred while fetching video details: {e}")
        best_single_format = None  # Ensure this is reset if there's an error
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        best_single_format = None  # Ensure this is reset if there's an error

# Download button and logic
if st.button("Download"):
    if url:
        try:
            # Define a temporary file path for saving the download on the server
            temp_file_path = os.path.join(os.getcwd(), 'downloaded_video.mp4')

            if best_single_format:
                format_id = best_single_format['format_id']

                # Download the best single format
                ydl_opts = {
                    'format': format_id,
                    'outtmpl': temp_file_path,
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                st.success("Download Complete!")

                # Provide a link to download the video file
                with open(temp_file_path, "rb") as file:
                    st.download_button(
                        label="Download Video",
                        data=file,
                        file_name=os.path.basename(temp_file_path),
                        mime="video/mp4"
                    )
                
                # Optionally, delete the file after the download
                os.remove(temp_file_path)

            else:
                st.error("No suitable format found for download.")
        except yt_dlp.utils.DownloadError as e:
            st.error(f"Download failed: {str(e)}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
    else:
        st.error("Please enter a YouTube URL.")
