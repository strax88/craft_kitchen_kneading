from fastapi import HTTPException, status


class CredentialHTTPException(HTTPException):
    """"""
    def __init__(self):
        """"""
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = f"Could not validate credentials"
    headers = {"WWW-Authenticate": "Bearer"}



class UserNotFoundHTTPException(CredentialHTTPException):
    """"""

    detail = f"User not found"



class IncorrectUsernamePasswordHTTPException(CredentialHTTPException):
    """"""

    detail = f"Incorrect username or password"



class InvalidRefreshTokenHTTPException(CredentialHTTPException):
    """"""

    detail = f"Invalid refresh token"
