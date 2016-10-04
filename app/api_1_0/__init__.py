from flask import Blueprint, request, g

api = Blueprint('api', __name__)

from ..models import User
from . import comments, error


@api.before_request
def before_api_request():
    if request.json is None:                                    #flask puts json decoded as dictionary in request.json
        return error.bad_request('Invalid JSON in body.')
    token = request.json.get('token')                           #get token from request
    if not token:
        return error.unauthorized('Authentication token not provided.')
    user = User.validate_api_token(token)                       #using staticmethod in models
    if not user:
        return error.unauthorized('Invalid authentication token.')
    g.current_user = user