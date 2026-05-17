# modules/auth/service.py

from modules.auth.repository import get_user


def login_user(username, password):

    user = get_user(
        username,
        password
    )

    if not user:
        return None

    if not user["active"]:
        return "inactive"

    return user