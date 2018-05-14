from __future__ import unicode_literals
from flask import abort, jsonify, Flask, make_response, request, send_from_directory
import os

from download import Download, Provider

app = Flask(__name__)
host = '127.0.0.1'
port = 8080

downloads = {}

@app.route('/', methods=['GET'])
def base():
    man = ('<pre><code>\n'
           'youtube-dl as a service\n'
           'POST outputDir [provider] [username] [password] url\n'
           '</code></pre>'
          )
    return man

@app.route('/downloads', methods=['GET'])
def get_downloads():
    return jsonify(list(downloads.keys()))

@app.route('/downloads', methods=['POST'])
def get_download_list():
    url = request.form['url']

    output_dir = os.getcwd()
    if 'outputDir' in request.form:
        base_dir = os.environ['BASE_DIR']
        output_dir = '{}/{}'.format(base_dir, request.form['outputDir'])

    provider = None
    # add authentication parameters if present in request
    if 'provider' in request.form:
        provider = Provider('Comcast_SSO', request.form['username'], request.form['password'])
        print('Setting up authentication using {}'.format(provider.mso))

    # queue download video
    print(f'Creating download task for: {url}')
    d = Download(url, output_dir, provider)
    downloads[d.download_id] = d
    # TODO: return proper url using download_id
    return jsonify(d.download_id)
    
@app.route('/downloads/<uuid:download_id>', methods=['GET'])
def get_download_by_id(download_id):
    print(f'Looking up download: {download_id}')
    if download_id not in downloads:
        abort(404)

    d = downloads[download_id]

    if d.process.exitcode == None:
        print('Download has not yet completed.')
        return make_response(f'{download_id} is still downloading', 202) 
    elif d.process.exitcode != 0:
        abort(500)

    if d.filename == None:
        print('Filename has not been set. Download still processing')
        # TODO: add progress and estimate remaining time
        return make_response(f'{download_id} is still processing', 202) 

    return send_from_directory(os.environ['BASE_DIR'],
                                d.filename, as_attachment=True)

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def f(url, output_dir, provider):
    info('function f')
    print(f'URL: {url} - Output Directory: {output_dir} - Provider - {provider}')
    download(url, output_dir, provider)
    
if __name__ == '__main__':
    info('main line')
    # starting web server
    print("Starting server")
    app.run(host=host, port=port)
