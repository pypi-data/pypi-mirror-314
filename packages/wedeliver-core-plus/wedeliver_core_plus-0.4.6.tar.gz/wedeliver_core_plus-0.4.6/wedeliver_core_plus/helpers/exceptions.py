class AppNoRowsFound(Exception):
    code = 404


class AppException(Exception):
    message = "Error"
    code = 500
    custom_exception = True
    silent = False
    use_default_response_message_key = True


class AppSilentException(AppException):
    silent = True


class AppNotSilentException(AppException):
    silent = False


class AppValidationError(AppSilentException):
    code = 400
    message = "Validation Error"


class AppNotSilentValidationError(AppNotSilentException):
    code = 400
    message = "Not Silent Validation Error"


class AppExpiredTokenError(AppSilentException):
    code = 401
    message = "Token Error"


class AppMicroFetcherError(AppSilentException):
    code = 400
    message = "Fetcher Service Error"


class AppThirdPartyError(AppNotSilentException):
    code = 400
    message = "Third Party Call Error"


class AppFetchServiceDataError(AppNotSilentException):
    code = 400
    message = "Error while fetch relational data from service"

    def __init__(self, message=None, code=None):
        if message:
            self.message = message
        if code:
            self.code = code


class AppNotFoundError(AppSilentException):
    code = 404
    message = "Not found"


class AppMissingAuthError(AppSilentException):
    code = 401
    message = "You are unauthenticated"


class AppDeprecatedApiError(AppSilentException):
    code = 410
    message = "This API is deprecated and no longer available"


class AppForbiddenError(AppSilentException):
    code = 403
    message = "You are not apple to use this API"


class CustomNotFoundError(AppSilentException):
    def __init__(self, message):
        self.message = message

    code = 404
