from modules.assets.repository import (
    get_assets_by_site,
    create_asset,
    get_asset_by_id
)


def list_assets(site_id):
    return get_assets_by_site(site_id)


def add_asset(name, type, site_id):
    if not name:
        return None

    create_asset(name, type, site_id)
    return True


def get_asset(asset_id):
    return get_asset_by_id(asset_id)