from conda.exceptions import CondaError


class CondaAuthError(CondaError):
    """Custom error for the conda-auth plugin"""


class InvalidCredentialsError(CondaAuthError):
    """Error raised when credentials are invalid"""