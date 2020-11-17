from __future__ import unicode_literals, print_function
import youtube_dl
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

ytdl_folder_id = '1Vr2a7lcAM8AyPH1rMIoNxzRSpPU2KoeN'

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

def gdrive_hook(d):
    if d['status'] == 'finished':
        output = drive.CreateFile(
            {'parents': [{'id': '1Vr2a7lcAM8AyPH1rMIoNxzRSpPU2KoeN'}]})
        output.SetContentFile(d['filename'])

        print('Uploading {0} to google drive.'.format(d['filename']))
        output.Upload()
        os.remove(d['filename'])


ydl_opts = {
    'download_archive': 'archive.txt',
    'playlistreverse': True,
    'ignoreerrors': True,
    'progress_hooks': [gdrive_hook]
    # 'extract_flat': True
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/playlist?list=FLmmnilMEPus-aUVc_xnmyHA'])
