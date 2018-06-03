from flask import flash, render_template, redirect, request, url_for
import requests
from werkzeug import secure_filename

from . import home
from .forms import DownloadForm

@home.route('/', methods=['GET'])
def base():
    form = DownloadForm()
    if form.validate_on_submit():
        return redirect(url_for('download'))

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
        if 'outputDir' not in data:
            data['outputDir'] = 'TODO'
        r = requests.post(url_for('api.get_download_list'), data = data)
        # output = r.json()
        # filename = output['filename']
        output = 'TODO'
        filename = 'TODO'
        info = {
            'data': data,
            'filename': filename,
            'output': output,
        }
        return render_template('download.html',
                                info=info)
    else:
        flash(error)

    return redirect(url_for('home.base'))
