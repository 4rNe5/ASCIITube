# Created By 4rNe5
# ASCIITube Code
# Creatred on 2023/06/13 - Tuesday

import cv2
import os
import sys
from pytube import YouTube

def download_video(url):
    yt = YouTube(url)
    video = yt.streams.filter(file_extension='mp4', res='360p').first()
    video.download(filename='temp_video.mp4')

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
    url = input("유튜브 영상 링크를 입력하세요 : ")
    download_video(url)
    try:
        video_to_ascii('temp_video.mp4', 'ascii_video.txt')
    finally:
        if os.path.exists('temp_video.mp4'):
            os.remove('temp_video.mp4')