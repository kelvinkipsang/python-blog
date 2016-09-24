from flask import Blueprint

talks = Blueprint('talks', __name__)

from . import routes        # "avoid" circular dependancies ie giving precedence to package constructor so that bprints are defined first

