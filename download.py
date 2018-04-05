from __future__ import unicode_literals
import youtube_dl
import os
from flask import abort, Flask, request
app = Flask(__name__)

output_format = '%(title)s.%(ext)s'

class ErrorLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

ydl_opts = {
    'download_archive': 'downloads.log',
    'format': 'best',
    'logger': ErrorLogger(),
    'progress_hooks': [],
}

@app.route('/', methods=['GET'])
def help():
    man = ('<pre><code>'
           '{}: youtube-dl as a service\n'
           'POST outputDir [provider] [username] [password] url'
           '</code></pre>'
          ).format(__name__)
    return man

@app.route('/', methods=['POST'])
def download():
    url = request.form['url']
    opts = ydl_opts

    # add authentication parameters if present in request

    if 'provider' in request.form:
        # TODO: setup proper provider -> ap_mso mapping
        opts['ap_mso'] = 'Comcast_SSO'
        print('Setting up authentication using {}'.format(opts['ap_mso']))
        opts['ap_username'] = request.form['username']
        opts['ap_password'] = request.form['password']

    output_dir = os.getcwd()
    if 'outputDir' in request.form:
        base_dir = os.environ['BASE_DIR']
        output_dir = '{}/{}'.format(base_dir, request.form['outputDir'])

    opts['outtmpl'] = output_dir + '/' + output_format

    # download video
    with youtube_dl.YoutubeDL(opts) as ydl:
        if ydl.download([url]) != 0:
            abort(500)

    return "Successfully downloaded to {}".format(output_dir)
