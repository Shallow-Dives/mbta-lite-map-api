from flask import Blueprint, jsonify

from .exceptions import ServerError

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(ServerError)
def server_error(error):
    message = [str(x) for x in error.args]
    status_code = error.status_code
    success = False
    response = {
        "success": success,
        "error": {"type": error.__class__.__name__, "message": message},
    }

    return jsonify(response), status_code
