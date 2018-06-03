from flask import flash, render_template, redirect, request, url_for

from . import home

@home.route('/', methods=['GET'])
def base():
    return render_template('index.html')

@home.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == 'POST':
        url = request.form['url']
        outputDir = request.form['outputDir']
        provider = request.form['provider']
        username = request.form['username']
        password = request.form['password']
        error = None

        if not url:
            error = 'Url is required'
        if not outputDir:
            error = 'Output directory is required'
        if provider:
            if not username:
                error = 'Username is required when using a provider'
            if not password:
                error = 'Password is required when using a provider'

        if error == None:
            return render_template('download.html')

        flash(error)

    return render_template('download.html')
