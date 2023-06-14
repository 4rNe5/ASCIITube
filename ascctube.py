import cv2
import os
import sys
import re
from pytube import YouTube

def is_valid_url(url):
    pattern = re.compile(r'(https?://)?(www\.)?youtube\.com/watch\?v=[\w-]{11}')
    return pattern.match(url) is not None

def download_video(url, resolution):
    yt = YouTube(url)
    video = yt.streams.filter(file_extension='mp4', res=resolution).first()
    if video is None:
        return False
    video.download(filename='temp_video.mp4')
    return True

def video_to_ascii(video_path, output_path, scale=0.1):
    cap = cv2.VideoCapture(video_path)
    ascii_chars = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized_frame = cv2.resize(gray_frame, (int(gray_frame.shape[1] * scale), int(gray_frame.shape[0] * scale)), interpolation=cv2.INTER_AREA)

        ascii_frame = ""
        for i in range(resized_frame.shape[0]):
            for j in range(resized_frame.shape[1]):
                pixel_value = resized_frame[i, j]
                ascii_frame += ascii_chars[pixel_value // 25]
            ascii_frame += "\n"

        os.system("cls" if os.name == "nt" else "clear")
        print(ascii_frame)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    while True:
        url = input("변환할 유튜브 영상의 링크를 입력하세요 : ")
        if is_valid_url(url):
            break
        else:
            print("올바른 유튜브 링크를 입력해주세요.")

    while True:
        resolution = input("다운로드할 영상의 해상도를 입력하세요 (예: 480p, 720p, 1080p): ")
        print("영상을 ASCII Art로 변환중입니다...")
        if download_video(url, resolution):
            break
        else:
            print("불가능한 해상도입니다. 다른 해상도를 지정해주세요.")

    try:
        video_to_ascii('temp_video.mp4', 'ascii_video.txt')
    finally:
        if os.path.exists('temp_video.mp4'):
            os.remove('temp_video.mp4')