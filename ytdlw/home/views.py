from flask import flash, render_template, redirect, request, url_for
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
    url = request.form['url']
    outputDir = None
    provider = None
    username = None
    password = None
    error = None

    if not url:
        error = 'Url is required'

    if 'outputDir' in request.form and request.form['outputDir']:
        outputDir = secure_filename(request.form['outputDir'])
    else:
        # TODO: resolve default path
        outputDir = 'TODO'

    if 'authenticate' in request.form and request.form['authenticate']:
        provider = request.form['provider']
        username = request.form['username']
        password = request.form['password']
        if not provider:
            error = 'Provider is required when using authentication'
        if not username:
            error = 'Username is required when using a provider'
        if not password:
            error = 'Password is required when using a provider'

    if error == None:
        # TODO: fire off download request to api
        # output = api.get_download_list
        output = "TODO: Download has been queued"
        info = {
            'url': url,
            'output': output,
            'outputDir': outputDir,
            'provider': provider,
            'username': username,
            'password': password,
        }
        return render_template('download.html',
                                download=info)
    else:
        flash(error)

    return redirect(url_for('home.base'))
