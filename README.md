# ytdlw #

youtube-dl web - A simple api and web wrapper for youtube-dl.


## Install ##

Clone the repo

```
git clone https://github.com/threePhase/ytdlw
cd ytdlw
```

Create a virtualenv and activate it:

```
python3 -m venv venv
. venv/bin/activate
```

Or on Windows cmd:

```
py -3 -m venv venv
venv\Scripts\activate.bat
```

Install ytdlw:

```
pip install -e .
```


## Developing ##

By default, `config.py` sets `SERVER_NAME` to `localhost` for ease of
development.

In order to test the subdomain blueprints locally, you must add the following
entry to your `/etc/hosts` file:

```
127.0.0.1       api.ytwdl.localhost

```


## Run ##

```
export FLASK_APP=ytdlw
export FLASK_ENV=development
flask run
```

Or on Windows cmd:

```
set FLASK_APP=ytdlw
set FLASK_ENV=development
flask run
```

Open http://api.ytdlw.localhost:5000 in a browser.


## Test ##

```
pip install '.[test]'
pytest
```

Run with coverage report:

```
coverage run -m pytest
coverage report
coverage html   # open htmlcov/index.html in a browser
```


## Caveats ##

Due to a
[longstanding issue on macOS](https://bugs.python.org/issue30385#msg293958),
Python applications that use `fork` must explicitly pass `env no_proxy='*'`
when invoking `flask run`, otherwise the application will crash when making a
download request to the API.
