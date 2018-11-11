""" Python Flask API Auth0 integration example
    Source: https://github.com/auth0-samples/auth0-python-api-samples/blob/master/00-Starter-Seed/server.py
"""

from functools import wraps
import json
from os import environ as env
from six.moves.urllib.request import urlopen

from dotenv import load_dotenv, find_dotenv
from flask import Flask, request, jsonify, _request_ctx_stack
from flask_cors import cross_origin
from jose import jwt

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
AUTH0_DOMAIN = env.get("AUTH0_DOMAIN")
API_IDENTIFIER = env.get("API_IDENTIFIER")
ALGORITHMS = ["RS256"]
APP = Flask(__name__)


# Format error response and append status code.
class AuthError(Exception):

    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


@APP.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


def get_token_auth_header():
    """Obtains the access token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({
            "code": "authorization_header_missing",
            "description": "Authorization header is expected"
        }, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({
            "code": "invalid_header",
            "description": "Authorization header must start with"
            " Bearer"
        }, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header", "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header", "description": "Authorization header must be" " Bearer token"}, 401)

    token = parts[1]
    return token


def check_required_scopes(required_scopes: str):
    """Determines if the required scope is present in the access token
    Args:
        required_scope (str): The scope required to access the resource
    """
    if not (required_scopes):
        return True

    token = get_token_auth_header()
    unverified_claims = jwt.get_unverified_claims(token)

    if unverified_claims.get("scope"):
        token_scopes = unverified_claims["scope"].split()
        required_scopes_list = required_scopes.split()
        for required_scope in required_scopes_list:
            if required_scope not in token_scopes:
                return False
        return True

    return False


def requires_auth(scopes=None):
    """Determines if the access token is valid
    """

    def decorator(f):
        # the actual decorator, which may use the variable "user"
        # (basically everything you've written, including the wrapper)
        @wraps(f)
        def decorated(*args, **kwargs):
            token = get_token_auth_header()
            jsonurl = urlopen("https://" + AUTH0_DOMAIN + "/.well-known/jwks.json")
            jwks = json.loads(jsonurl.read())
            try:
                unverified_header = jwt.get_unverified_header(token)
            except jwt.JWTError:
                raise AuthError({
                    "code": "invalid_header",
                    "description": "Invalid header. "
                    "Use an RS256 signed JWT Access Token"
                }, 401)
            if unverified_header["alg"] == "HS256":
                raise AuthError({
                    "code": "invalid_header",
                    "description": "Invalid header. "
                    "Use an RS256 signed JWT Access Token"
                }, 401)
            rsa_key = {}
            for key in jwks["keys"]:
                if key["kid"] == unverified_header["kid"]:
                    rsa_key = {"kty": key["kty"], "kid": key["kid"], "use": key["use"], "n": key["n"], "e": key["e"]}
            if rsa_key:
                try:
                    payload = jwt.decode(
                        token,
                        rsa_key,
                        algorithms=ALGORITHMS,
                        audience=API_IDENTIFIER,
                        issuer="https://" + AUTH0_DOMAIN + "/")
                except jwt.ExpiredSignatureError:
                    raise AuthError({"code": "token_expired", "description": "token is expired"}, 401)
                except jwt.JWTClaimsError:
                    raise AuthError({
                        "code": "invalid_claims",
                        "description": "incorrect claims,"
                        " please check the audience and issuer"
                    }, 401)
                except Exception:
                    raise AuthError({
                        "code": "invalid_header",
                        "description": "Unable to parse authentication"
                        " token."
                    }, 401)

                if (not check_required_scopes(scopes)):
                    raise AuthError({
                        "code": "invalid scope",
                        "description": "No access to scope"
                        " please check the scope"
                    }, 403)
                _request_ctx_stack.top.current_user = payload
                return f(*args, **kwargs)
            raise AuthError({"code": "invalid_header", "description": "Unable to find appropriate key"}, 401)

        return decorated

    return decorator


# Controllers API
@APP.route("/api/public")
@cross_origin(headers=["Content-Type", "Authorization"])
def public():
    """No access token required to access this route
    """
    response = "Hello from a public endpoint! You don't need to be authenticated to see this."
    return jsonify(message=response)


@APP.route("/api/private")
@cross_origin(headers=["Content-Type", "Authorization"])
@cross_origin(headers=["Access-Control-Allow-Origin", "http://localhost:3000"])
@requires_auth()
def private():
    """A valid access token is required to access this route
    """
    response = "Hello from a private endpoint! You are authenticated to see this."
    return jsonify(message=response)


@APP.route("/api/update", methods=['PUT'])
@cross_origin(headers=["Content-Type", "Authorization"])
@cross_origin(headers=["Access-Control-Allow-Origin", "http://localhost:3000"])
@requires_auth('update:syslog')
def update():
    req_data = request.get_json()
    """A valid access token and an appropriate scope are required to access this route
    """
    response = "Hello from a private endpoint! You are authenticated and have a scope of update:syslog.\n Values are\
     \nKey1: {}\nKey2: {}".format(req_data['key1'], req_data['key2'])
    return jsonify(message=response)


@APP.route("/api/read")
@cross_origin(headers=["Content-Type", "Authorization"])
@cross_origin(headers=["Access-Control-Allow-Origin", "http://localhost:3000"])
@requires_auth(' read:syslog')
def read():
    """A valid access token and an appropriate scope are required to access this route
    """
    response = "Hello from a private endpoint! You are authenticated and have access to read:syslog"
    return jsonify(message=response, data={"key1": "value1", "key2": "value2"})


@APP.route("/api/readupdate")
@cross_origin(headers=["Content-Type", "Authorization"])
@cross_origin(headers=["Access-Control-Allow-Origin", "http://localhost:3000"])
@requires_auth('update:syslog read:syslog')
def readupdate():
    """A valid access token and an appropriate scope are required to access this route
    """
    response = "Hello from a private endpoint! You are authenticated and have access to update:syslog read:syslog"
    return jsonify(message=response)


@APP.route("/api/noaccess")
@cross_origin(headers=["Content-Type", "Authorization"])
@cross_origin(headers=["Access-Control-Allow-Origin", "http://localhost:3000"])
@requires_auth('no:access update:syslog')
def noaccess():
    """A valid access token and an appropriate scope are required to access this route
    """
    response = "Hello from a private endpoint! You are authenticated and have a scope of no:access"
    return jsonify(message=response)


if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=env.get("PORT", 3010))
