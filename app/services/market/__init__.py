from flask import Response, jsonify
from typing import Tuple
from app.utils.io import get_creation_params, get_pagination_params, get_filter_params, get_sort_params, get_update_params
from app.services.market.get_profile_accessories import get_profile_accessories
from app.services.market.create_profile_accessories import create_profile_accessories
from app.services.market.update_profile_accessories import update_profile_accessories
from app.services.market.delete_profile_accessories import delete_profile_accessories


def get_profile_accessories_service() -> Tuple[Response, int]:
    """
    Service function to get all profile accessories.

    :return: Tuple with response and status code.
    """
    page, per_page = get_pagination_params()
    filters = get_filter_params()
    sorting = get_sort_params()
    return get_profile_accessories(page=page, per_page=per_page, filters=filters, sorting=sorting)

# ----------------- CREATE MARKET ITEM ----------------- #
def create_profile_accessories_service() -> Tuple[Response, int]:
    """
    Service function to create a new market item.

    :return: Tuple with response and status code.
    """
    try:
        creation_params = get_creation_params(force=True)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return create_profile_accessories(creation_obj=creation_params)

# ----------------- UPDATE MARKET ITEM ----------------- #
def update_profile_accessories_service(item_id: str) -> Tuple[Response, int]:
    """
    Service function to update a market item.

    :return: Tuple with response and status code.
    """
    try:
        update_params = get_update_params(force=True)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return update_profile_accessories(item_id=item_id, update_obj=update_params)

# ----------------- DELETE MARKET ITEM ----------------- #
def delete_profile_accessories_service(item_id: str) -> Tuple[Response, int]:
    """
    Service function to delete a market item.

    :return: Tuple with response and status code.
    """
    return delete_profile_accessories(item_id=item_id)
