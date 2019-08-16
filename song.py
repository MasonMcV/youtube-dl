import pafy

from pydub import AudioSegment
import urllib
import os
import time


def removeNonAscii(s): return "".join(i for i in s if ord(i) < 128)


apifile = open("api_key.txt", "r")
key = apifile.readline()

if __name__ == '__main__':

    f = open("songs.txt", "r")

    if not f.mode == 'r':
        print ("Failed to open songs.txt, please make sure it exists")
        exit(-1)

    for line in f.readlines():
        url = line.split(' ')
        print (url)

        if url[0][0] == '#':
            continue

        url = url[0]

        pafy.set_api_key(key)

        video = pafy.new(url, gdata=True)

        audio = video.getbestaudio()

        # audio = video.audiostreams
        # audio = audio[-1]


        def mycb(total, recvd, ratio, rate, eta):
            print (recvd / 1024, "kb Received out of ", total / 1024, "kb - ", '{0:3.1f}'.format(
                ratio * 100), " ", '{0:3.1f}'.format(eta), " Seconds left")

        audio.download(callback=mycb)

        urllib.urlretrieve(video.bigthumbhd, "thumb.jpg")

        file = AudioSegment.from_file(video.title + '.' + audio.extension, format=audio.extension)

        print (video.title.split(' - ')[1], video.title.split(' - ')[0], video.published, video.thumb)

        if not os.path.exists("songs"):
            os.mkdir("songs")

        file.export("songs/" + video.title + '.' + "mp3", format='mp3', tags={
            "title": removeNonAscii(video.title.split(' - ')[1]),
            "artist": removeNonAscii(video.title.split(' - ')[0]),
            'year': video.published[:4]
        }, cover="thumb.jpg")

        os.remove(video.title + '.' + audio.extension)

    os.remove("thumb.jpg")
