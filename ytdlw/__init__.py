import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True,
        subdomain_matching=True)

    # load default configuration
    app.config.from_object('config')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass

    # setup api blueprint
    from .api import api
    # place API blueprint on 'api.' subdomain
    app.register_blueprint(api, subdomain='api')

    return app
