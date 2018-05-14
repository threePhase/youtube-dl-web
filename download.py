from multiprocessing import Process
import os
import uuid
import youtube_dl

output_format = '%(title)s.%(ext)s'

class ErrorLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

class Download(object):
    """Encapsulates youtube-dl download task"""
    def __init__(self, url, output_dir, provider):
        self.output_dir = output_dir
        self.provider = provider
        self.url = url

        self.download_id = uuid.uuid4()

        self.filename = None
        def finished_hook(d):
            if d['status'] == 'finished':
                self.filename = d['filename']
                print(f'Finished downloading: {self.filename}')

        self.process = Process(target=download, name=f'{self.download_id}',
            args=(url, output_dir, provider, finished_hook,))
        self.process.start()

class Provider(object):
    """Encapsulates youtube-dl provider data"""
    def __init__(self, provider, username, password):
        # TODO: setup proper provider -> ap_mso mapping
        self.mso = provider
        self.ap_username = username
        self.ap_password = password

ydl_opts = {
    'download_archive': 'downloads.log',
    'format': 'best',
    'logger': ErrorLogger(),
    'progress_hooks': [],
}

def download(url, output_dir, provider, finished_hook):
    opts = ydl_opts

    opts['outtmpl'] = output_dir + '/' + output_format

    opts['progress_hooks'] = [finished_hook]

    if provider:
        opts['ap_mso'] = provider.mso
        opts['ap_username'] = provider.ap_username
        opts['ap_password'] = provider.ap_password

    with youtube_dl.YoutubeDL(opts) as ydl:
        print(f'Downloading: {url}')
        return ydl.download([url])


