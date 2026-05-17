# modules/auth/service.py

from modules.auth.repository import (
    get_user,
    insert_user
)


# =========================================
# LOGIN
# =========================================
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


# =========================================
# CREATE USER
# =========================================
def create_user(
    username,
    password,
    role,
    company_id
):

    return insert_user(
        username,
        password,
        role,
        company_id
    )