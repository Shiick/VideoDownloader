from pytube import YouTube
from moviepy.editor import *
import shutil
import requests

def check_video_url(video_url):
    checker_url = "https://www.youtube.com/oembed?url="
    video_url = checker_url + video_url
    request = requests.get(video_url)
    return request.status_code == 200

def main():
    with open("input.txt") as file_in:
        for line in file_in:
            video = YouTube(line.replace("\\n", ""))
            if (check_video_url(line.replace("\\n", ""))):
                versions = video.streams.filter(file_extension="mp4").order_by('resolution')[::-1]
                if (versions[0].includes_audio_track):
                    print("Best quality and best audio currently downloading. {0}".format(versions[0].default_filename))
                    versions[0].download()
                    print("Video downloaded! Video is available. {0}".format(versions[0].default_filename))
                else:
                    print("Downloading best video quality. {0}".format(versions[0].default_filename))
                    versions[0].download(output_path="Video")
                    print("Downloaded best video quality.")
                    for stream in versions:
                        if (stream.includes_audio_track):
                            print("Downloading best audio quality. {0}".format(versions[0].default_filename))
                            stream.download(output_path="Audio")
                            print("Downloaded best audio quality.")
                            videoclip = VideoFileClip("Video\\{0}".format(versions[0].default_filename))
                            audioclip = VideoFileClip("Audio\\{0}".format(versions[0].default_filename)).audio

                            videoclip.audio = audioclip
                            print("Combining best quality and best audio together.")
                            videoclip.write_videofile(versions[0].default_filename)
                            shutil.rmtree("Video")
                            shutil.rmtree("Audio")
                            print("Video combined! Video is available. {0}".format(versions[0].default_filename))
                            break
            else:
                print("Not a valid URL.")

if __name__ == "__main__":
    main()
