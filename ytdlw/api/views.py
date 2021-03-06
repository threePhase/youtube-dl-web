from __future__ import unicode_literals
from flask import abort, jsonify, Flask, make_response, request, \
    send_from_directory, url_for
from multiprocessing import Pool
import os
import urllib.parse
import uuid

from .download import Download, Provider
from . import api

downloads = {}
pool = Pool()
man = ('<pre><code>\n'
       'youtube-dl as a service\n'
       'POST outputDir [provider] [username] [password] url\n'
       '</code></pre>'
      )

@api.route('/', methods=['GET', 'POST'])
def base():
    if request.method == 'GET':
        return man
    else:
        url = request.form['url']

        output_dir = os.environ['BASE_DIR']
        if 'outputDir' in request.form:
            output_dir = '{}/{}'.format(output_dir, request.form['outputDir'])

        provider = None
        # add authentication parameters if present in request
        if 'provider' in request.form:
            provider = Provider('Comcast_SSO', request.form['username'], request.form['password'])
            print('Setting up authentication using {}'.format(provider.mso))

        # queue download video
        print(f'Creating download task for: {url}')

        download_id = uuid.uuid4()
        downloads[download_id] = pool.apply_async(Download,
            (download_id, url, output_dir, provider,))

        url = url_for('.get_download_by_id',
                        download_id=download_id,
                        _external=True)
        return f'{url}'

@api.route('/downloads', methods=['GET'])
def get_downloads():
    return jsonify(list(downloads.keys()))
    
@api.route('/downloads/<uuid:download_id>', methods=['GET'])
def get_download_by_id(download_id):
    print(f'Looking up download: {download_id}')
    if download_id not in downloads:
        abort(404)

    d = downloads[download_id]

    if not d.ready():
        print('Download has not yet completed.')
        return make_response(f'{download_id} is still downloading', 202) 

    if not d.successful():
        print('Download failed unexpectedly.')
        d.get()
        abort(500)

    download = d.get()

    print(f"Sending {os.path.join(download.base_dir, download.basename)} for ID: {download_id}")

    # TODO: verify file exists before attempting to send
    return send_from_directory(download.base_dir, download.basename, as_attachment=True)

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())
