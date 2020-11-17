# TO DO:
# - use service account instead of oauth client as described
#   here: https://stackoverflow.com/questions/46457093/
# - add script to crontab


from __future__ import unicode_literals, print_function
import youtube_dl
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

gdrive_folder_id = '1Vr2a7lcAM8AyPH1rMIoNxzRSpPU2KoeN'
yt_playlist_id = 'FLmmnilMEPus-aUVc_xnmyHA'
data_dir = './data/'


def gdrive_hook(d):
    if d['status'] == 'finished':
        title = d['filename'].replace(data_dir, '')
        output = drive.CreateFile({
            'title': title,
            'parents': [{'id': gdrive_folder_id}]})
        output.SetContentFile(d['filename'])

        print('Uploading {0} to google drive.'.format(title))
        output.Upload()
        os.remove(d['filename'])


def main(ydl_opts):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.youtube.com/playlist?list={0}'.format(
            yt_playlist_id)])


if __name__ == '__main__':

    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    ydl_opts = {
        'format': 'bestvideo/best',
        'download_archive': 'archive.txt',
        'playlistreverse': True,
        'ignoreerrors': True,
        'progress_hooks': [gdrive_hook],
        'restrictfilenames': True,
        'outtmpl': './data/%(title)s-%(id)s.%(ext)s'
    }
    main(ydl_opts)
