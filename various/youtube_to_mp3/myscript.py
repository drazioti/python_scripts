from __future__ import unicode_literals
import sys
sys.path.insert(0,'/path/to/youtube-dl')
import youtube_dl

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}

fo = open("list.txt", "r")
lines = fo.readlines()
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    for line in lines:
        ydl.download([line])

