import os

from dapla.auth import AuthClient

from dapla_suv_tools._internals.util.suv_operation_context import SuvOperationContext
from dapla_suv_tools._internals.util import constants


def get_access_token(context: SuvOperationContext) -> str:
    if os.getenv("LOCAL_DEV_ACTIVE", None):
        return os.getenv("SUV_LOCAL_TOKEN", "")

    context.log(level=constants.LOG_DIAGNOSTIC, message="Fetching user access_token")
    return AuthClient.fetch_personal_token()


def get_current_user(context: SuvOperationContext) -> str:
    if os.getenv("LOCAL_DEV_ACTIVE", None):
        return os.getenv("SUV_LOCAL_USER", "")

    context.log(level=constants.LOG_DIAGNOSTIC, message="Fetching email")
    local_user = AuthClient.fetch_email_from_credentials()
    return local_user if local_user else "unknown"
