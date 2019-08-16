import pafy

from pydub import AudioSegment
import urllib
import os

def removeNonAscii(s): return "".join(i for i in s if ord(i) < 128)

if __name__ == '__main__':

    f = open("songs.txt", "r")

    if not f.mode == 'r':
        print "Failed to open songs.txt, please make sure it exists"
        exit(-1)

    for line in f.readlines():

        url = line

        video = pafy.new(url, gdata=True)

        audio = video.getbestaudio()


        def mycb(total, recvd, ratio, rate, eta):
            print(recvd, ratio, eta)

        # audio.download(callback=mycb)

        urllib.urlretrieve(video.bigthumbhd, "thumb.jpg")

        file = AudioSegment.from_file(video.title + '.' + audio.extension, format=audio.extension)

        print video.title.split(' - ')[1], video.title.split(' - ')[0], video.published, video.thumb

        file.export(video.title + '.' + "mp3", format='mp3', tags={
            "title": removeNonAscii(video.title.split(' - ')[1]),
            "artist": removeNonAscii(video.title.split(' - ')[0]),
            'year': video.published[:4]
        }, cover="thumb.jpg")
        os.remove(video.title + '.' + audio.extension)

    os.remove("thumb.jpg")
