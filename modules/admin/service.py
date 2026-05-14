from modules.admin.repository import (
    get_all_users,
    update_user_status,
    create_company,
    create_user
)


def list_users():
    return get_all_users()


def toggle_user(user_id, active):
    update_user_status(user_id, active)


def register_company_and_user(
    company_name,
    username,
    password,
    role
):

    company_id = create_company(company_name)

    create_user(
        username,
        password,
        role,
        company_id
    )