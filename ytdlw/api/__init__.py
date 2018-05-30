from flask import Blueprint

api = Blueprint(
    'site',
    __name__,
)

from . import views
