import os
import youtube_dl

output_format = '%(title)s.%(ext)s'

class ErrorLogger(object):
    """Error ONLY logger for YouTubeDL"""
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

class Download(object):
    """Encapsulates youtube-dl download task"""
    def __init__(self, download_id, url, output_dir, provider):
        self.output_dir = output_dir
        self.provider = provider
        self.url = url
        self.download_id = download_id
        self.dir = None
        self.basename = None

        self.download()

    def download(self):
        opts = {
            #'download_archive': 'downloads.log',
            'format': 'best',
            'logger': ErrorLogger(),
            'progress_hooks': [],
        }

        opts['outtmpl'] = self.output_dir + '/' + output_format
        print(f"Output format: {opts['outtmpl']}")

        opts['progress_hooks'] = [self.finished_hook]

        if self.provider:
            opts['ap_mso'] = self.provider.mso
            opts['ap_username'] = self.provider.ap_username
            opts['ap_password'] = self.provider.ap_password

        with youtube_dl.YoutubeDL(opts) as ydl:
            print(f'Downloading: {self.url}')
            return ydl.download([self.url])

    def finished_hook(self, d):
        if d['status'] == 'finished':
            filename = d['filename']
            self.base_dir = os.path.dirname(filename)
            self.basename = os.path.basename(filename)
            print(f'Finished downloading: {filename}')

class Provider(object):
    """Encapsulates youtube-dl provider data"""
    def __init__(self, provider, username, password):
        # TODO: setup proper provider -> ap_mso mapping
        self.mso = provider
        self.ap_username = username
        self.ap_password = password

