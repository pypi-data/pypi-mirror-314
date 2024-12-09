from flask import request, g

from flask import session

from .authenticate import authenticate
from .micro_fetcher import MicroFetcher


class Auth:
    def __init__(self):
        pass

    @staticmethod
    def set_user(user):
        """
        Set user in flask global object and session
        """
        g.user = user  # store user in flask global object
        session["user"] = user

    @staticmethod
    def get_user():
        default_user_str = 'administrator@wedeliverapp.com'
        try:
            user = session.get("user", dict())
        except Exception:
            user = dict(user_id=default_user_str, email=default_user_str)

        return user

    @staticmethod
    def get_user_language():
        user = Auth.get_user()

        return user.get('language', 'en')

    @staticmethod
    def get_user_str():
        # app = WedeliverCorePlus.get_app()
        # with app.test_request_context():
        user = Auth.get_user()

        if user.get('email'):
            return user.get('email')
        else:
            return "Account-{}".format(
                user.get("account_id")
            )


def verify_user_token_v2(token):
    results = MicroFetcher(
        "AUTH_SERVICE"
    ).from_function(
        "app.business_logic.auth.authenticate.authenticate"
    ).with_params(
        token=token
    ).fetch()

    results["data"].update(token=token)
    user = results["data"]

    # get language form accept language in header of request
    try:
        language = (
            request.headers["Accept-Language"].lower()
            if (
                    "Accept-Language" in request.headers
                    and request.headers["Accept-Language"] in ["en", "ar"]
            )
            else (user.get("language") or 'ar')
        )
    except Exception:
        language = 'ar'

    user["language"] = language

    Auth.set_user(user)

    return user


def verify_user_token_v3(token):
    results = authenticate(token)

    results["data"].update(token=token)
    user = results["data"]

    # get language form accept language in header of request
    try:
        language = (
            request.headers["Accept-Language"].lower()
            if (
                    "Accept-Language" in request.headers
                    and request.headers["Accept-Language"] in ["en", "ar"]
            )
            else (user.get("language") or 'ar')
        )
    except Exception:
        language = 'ar'

    user["language"] = language

    Auth.set_user(user)

    return user
