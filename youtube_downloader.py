import time
from bs4 import BeautifulSoup
from pytube import YouTube
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def get_video_urls(user_url):
    driver_path = "/opt/homebrew/bin/chromedriver"

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    driver.get(user_url + "/videos")

    popular_videos_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//yt-formatted-string[contains(text(), '人気の動画')]"))
    )
    popular_videos_link.click()
    print("clicked popular videos link. waiting for 5 seconds...")
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    video_urls = []
    for link in soup.find_all("a", class_="yt-simple-endpoint style-scope ytd-grid-video-renderer"):
        video_url = f"https://www.youtube.com{link['href']}"
        video_urls.append(video_url)

    driver.quit()
    return video_urls[:30]

def download_video(url):
    try:
        video = YouTube(url)
        stream = video.streams.get_highest_resolution()
        print(f"ダウンロード中: {video.title}")
        stream.download()
        print("ダウンロード完了!")

    except Exception as e:
        print(f"エラー: {str(e)}")

def main():
    user_url = "https://www.youtube.com/@xxxxxxxxxxx"
    #video_urls = get_video_urls(user_url)
    video_urls = [
        "https://www.youtube.com/watch?v=xxxxxxxxxx",
    ]
    print("video_urls:", video_urls)
    for url in video_urls:
        download_video(url)
    print("All videos downloaded!")

if __name__ == "__main__":
    main()
