import subprocess

def main():
    # Execute YouTube video download process
    print("Starting YouTube video download...")
    subprocess.run(['python', 'youtube_downloader.py'], check=True)

    # Convert downloaded MP4 files to MP3 format  
    print("\nConverting MP4 files to MP3...")  
    subprocess.run(['python', 'mp4_to_mp3.py'], check=True)  
    
    # Transcribe MP3 audio files to text using ReazonSpeech  
    print("\nTranscribing MP3 files to text...")  
    subprocess.run(['python', 'mp3_to_txt_reazon.py'], check=True)  
    
    print("\nAll processes completed successfully!")  

if __name__ == "__main__":
    main()
