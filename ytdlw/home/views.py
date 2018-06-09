from flask import flash, render_template, redirect, request, url_for
import requests
from werkzeug import secure_filename

from . import home
from .models import Download
from .forms import DownloadForm

@home.route('/', methods=['GET'])
def base():
    form = DownloadForm()
    if form.validate_on_submit():
        return redirect(url_for('.download'))

    return render_template('index.html', form=form)

@home.route('/download', methods=['POST'])
def download():
    error = None
    if 'url' not in request.form:
        error = 'Url is required'

    data = { 'url' : request.form['url'] }

    if 'outputDir' in request.form and request.form['outputDir']:
        data['outputDir'] = secure_filename(request.form['outputDir'])

    if 'authenticate' in request.form and request.form['authenticate']:
        if 'provider' not in request.form and request.form['provider']:
            error = 'Provider is required when using authentication'
        if 'username' not in request.form and request.form['username']:
            error = 'Username is required when using a provider'
        if 'password' not in request.form and request.form['password']:
            error = 'Password is required when using a provider'

        data['provider'] = request.form['provider']
        data['username'] = request.form['username']
        data['password'] = request.form['password']

    if error == None:
        r = requests.post(url_for('api.base'), data = data)
        # output = r.json()
        # link = output['link']
        output = r.text
        link = r.text
        info = {
            'data': data,
            'link': link,
            'output': output,
        }
        return render_template('download.html',
                                info=info)
    else:
        flash(error)

    return redirect(url_for('.base'))

@home.route('/downloads', methods=['GET'])
def downloads():
    r = requests.get(url_for('api.get_downloads'))
    downloads = []
    for download_id in r.json():
        url = url_for('api.get_download_by_id', download_id=download_id, _external=True)
        downloads.append(Download(download_id, url))
    return render_template('downloads.html', downloads=downloads)
