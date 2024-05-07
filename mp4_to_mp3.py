import os
import subprocess

def convert_mp4_to_mp3(mp4_folder, mp3_folder):

    os.makedirs(mp3_folder, exist_ok=True)
    for root, dirs, files in os.walk(mp4_folder):
        for file in files:
            if file.endswith(".mp4"):
                mp4_path = os.path.join(root, file)
                mp3_filename = os.path.splitext(file)[0] + ".mp3"
                mp3_path = os.path.join(mp3_folder, mp3_filename)

                command = [
                    "ffmpeg",
                    "-i", mp4_path,
                    "-b:a", "256k",
                    "-vn",
                    mp3_path
                ]

                subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                print(f"Conversion complete: {mp4_path} -> {mp3_path}")

def main():
    mp4_folder = "./mp4"
    mp3_folder = "./mp3"
    if not os.path.exists(mp4_folder, mp3_folder):
        print("no folder found. exiting...")
        return

    convert_mp4_to_mp3(mp4_folder, mp3_folder)
    print("all mp4 files converted to mp3!")

if __name__ == "__main__":
    main()
