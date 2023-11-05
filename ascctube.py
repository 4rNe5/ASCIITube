import cv2
import os
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

def video_to_ascii(video_path, output_path):
    cap = cv2.VideoCapture(video_path)
    ascii_chars = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # (1) Calculate the aspect ratio and resize the frame accordingly
        aspect_ratio = gray_frame.shape[1] / gray_frame.shape[0]
        new_width = 120
        new_height = int(new_width / aspect_ratio)
        resized_frame = cv2.resize(gray_frame, (new_width, new_height), interpolation=cv2.INTER_AREA)

        ascii_frame = ""
        for i in range(resized_frame.shape[0]):
            for j in range(resized_frame.shape[1]):
                pixel_value = resized_frame[i, j]
                ascii_frame += ascii_chars[pixel_value // 25]
            ascii_frame += "\n"

        os.system("cls" if os.name == "nt" else "clear")
        print(ascii_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    while True:
        url = input("Input Youtube Video Link for Convert to ASCII Art : ")
        if is_valid_url(url):
            break
        else:
            print("Uncorrect URL. Please Enter Correct URL")

    while True:
        resolution = input("Input Video Resolution (ex: 480p, 720p...) : ")
        print("Convert Video to ASCII Art.....")
        if download_video(url, resolution):
            break
        else:
            print("Uncorrect Resolution. Please Enter Available Resolution")

    try:
        video_to_ascii('temp_video.mp4', 'ascii_video.txt')
    finally:
        if os.path.exists('temp_video.mp4'):
            os.remove('temp_video.mp4')
            print("")
