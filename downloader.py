from pytube import YouTube
from pydub import AudioSegment
import os
import string
import time

def download_audio(link, output_dir, retries = 3):
    for attempt in range(retries):
        try:
            youtube_object = YouTube(link)
            title = youtube_object.title

            valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
            safe_title = ''.join(c if c in valid_chars else '_' for c in title)

            audio_stream = youtube_object.streams.filter(only_audio=True).first()

            if not audio_stream:
                print("There is no audio stream for the link.")
                return

            audio_file = audio_stream.download(output_path=output_dir, filename="audio")

            audio = AudioSegment.from_file(audio_file)
            mp3_file = os.path.join(output_dir, f"{safe_title}.mp3")
            audio.export(mp3_file, format="mp3")

            os.remove(audio_file)

            print(f"The MP3 is saved as: {mp3_file}")
            return
        except Exception as e:
            print(f"Error: {e}. Attempt {attempt + 1} of {retries}.")
            time.sleep(5)
    print("I'm sorry I can't make it. Check for pytube updates. Bye 4 now")
    time.sleep(5)

if __name__ == "__main__":
    print("Welcome. Enter links. To escape enter e as a link and press the enter ")
    output_directory = input("Enter the output dir: ")
    output_directory = output_directory.replace('"', "")

    if not os.path.exists(output_directory):
        print("The directory that you have entered doesn't exist. ")
        output_directory = input("Enter a new path: ")
        if not os.path.exists(output_directory):
            print("It still doesn't exist. Bye")
            exit()

    tab = []

    while True:
        x = input("Enter a link: ")
        if x == "e":
            break
        else:
            if 'youtube.com' in x or 'youtu.be' in x:
                tab.append(x)
            else:
                print("Wrong link. Try again.")

    for i in tab:
        download_audio(i, output_directory)