from typing import List

from anyscale._private.sdk import sdk_command
from anyscale.user._private.user_sdk import PrivateUserSDK
from anyscale.user.models import AdminCreatedUser, AdminCreateUser


_USER_SDK_SINGLETON_KEY = "user_sdk"

_ADMIN_BATCH_CREATE_EXAMPLE = """
import anyscale
from anyscale.user.models import AdminCreateUser

anyscale.user.admin_batch_create(
    [AdminCreateUser(
        name="name",
        email="test@anyscale.com",
        password="",
        is_sso_user=False,
        lastname="lastname",
        title="title",
    ),],
)
"""

_ADMIN_BATCH_CREATE_ARG_DOCSTRINGS = {
    "admin_create_users": "Users to be created by an admin.",
}


@sdk_command(
    _USER_SDK_SINGLETON_KEY,
    PrivateUserSDK,
    doc_py_example=_ADMIN_BATCH_CREATE_EXAMPLE,
    arg_docstrings=_ADMIN_BATCH_CREATE_ARG_DOCSTRINGS,
)
def admin_batch_create(
    admin_create_users: List[AdminCreateUser], *, _sdk: PrivateUserSDK
) -> List[AdminCreatedUser]:
    """Batch create users without email verification as an admin.
    """
    return _sdk.admin_batch_create(admin_create_users)
