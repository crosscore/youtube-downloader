import yt_dlp
import os

def download_youtube_video(url, output_dir):
    ydl_opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Download completed.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    video_url = input("Please input YouTube URL: ")
    output_dir = "mp4"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    download_youtube_video(video_url, output_dir)