from modules.companies.repository import (
    get_companies,
    get_company_by_id,
    create_company
)


def list_companies():
    return get_companies()


def get_company(company_id):
    return get_company_by_id(company_id)


def add_company(name):
    if not name:
        return None

    create_company(name)
    return True