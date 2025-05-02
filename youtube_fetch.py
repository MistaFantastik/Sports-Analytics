import os
from googleapiclient.discovery import build
import yt_dlp

# Replace with your YouTube API key
API_KEY = "AIzaSyB7MI1dhj_8c5RvlYezSB0kzy7hZNxlbEg"

# Initialize YouTube API client
youtube = build("youtube", "v3", developerKey=API_KEY)

def search_youtube(query, max_results=3):
    """Search YouTube for videos and return a list of video URLs."""
    request = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=max_results
    )
    response = request.execute()

    videos = []
    for item in response["items"]:
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        url = f"https://www.youtube.com/watch?v={video_id}"
        videos.append({"title": title, "url": url})
    
    return videos

def download_video(video_url, output_dir="downloads"):
    """Download the video using yt-dlp and return the file path."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ydl_opts = {
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',  # Save with the correct title
        'format': 'bestvideo+bestaudio/best',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
        file_path = f"{output_dir}/{info_dict['title']}.{info_dict['ext']}"
        print(f"✅ Download complete: {file_path}")
        return file_path  # Return the downloaded file path
