import os
from moviepy.editor import *

def convert_mp4_to_mp3(mp4_path, mp3_path):
    video = VideoFileClip(mp4_path)
    video.audio.write_audiofile(mp3_path)

def main():
    mp4_folder = 'mp4_files'
    mp3_folder = 'mp3_files'

    # フォルダが存在しない場合は作成
    if not os.path.exists(mp4_folder):
        os.makedirs(mp4_folder)
    if not os.path.exists(mp3_folder):
        os.makedirs(mp3_folder)

    for filename in os.listdir(mp4_folder):
        if filename.endswith(".mp4"):
            mp4_path = os.path.join(mp4_folder, filename)
            mp3_path = os.path.join(mp3_folder, os.path.splitext(filename)[0] + '.mp3')
            convert_mp4_to_mp3(mp4_path, mp3_path)

if __name__ == "__main__":
    main()
