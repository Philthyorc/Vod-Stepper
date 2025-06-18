# vod_stepper/test_downloader.py

from downloader import download_video

if __name__ == "__main__":
    url = input("Paste a YouTube VOD URL: ")
    path = download_video(url)
    print(f"✅ Video downloaded to: {path}")
