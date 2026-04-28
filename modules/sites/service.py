from modules.sites.repository import (
    get_sites_by_company,
    create_site,
    get_site_by_id
)


def list_sites(company_id):
    return get_sites_by_company(company_id)


def add_site(name, company_id):
    if not name:
        return None

    create_site(name, company_id)
    return True


def get_site(site_id):
    return get_site_by_id(site_id)