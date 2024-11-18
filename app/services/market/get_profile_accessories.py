from sqlalchemy import and_
from typing import Optional, Tuple, Dict, Any
from flask import Response, jsonify
from app.models import ProfileAccessories
from app.utils.io import paginate_query, build_filter_conditions, build_sort_conditions
from app.types.mappings.filters import PROFILE_ACCESSORIES_FILTER_MAPPINGS
from app.types.mappings.sorting import PROFILE_ACCESSORIES_SORTING_MAPPINGS

def get_profile_accessories(page: int, per_page: int, filters: Optional[Dict[str, Any]] = None, sorting: Optional[Dict[str, Any]] = None) -> Tuple[Response, int]:
    """
    Get all profile accessories with optional filters.

    :param page: Current page number.
    :param per_page: Number of items per page.
    :param filters: Optional dictionary with filter criteria.
    :return: Tuple with response and status code.
    """
    try:
        # Build filter conditions
        filter_conditions = build_filter_conditions(ProfileAccessories, filters, PROFILE_ACCESSORIES_FILTER_MAPPINGS) if filters else []

        # Build sort conditions
        sort_conditions = build_sort_conditions(ProfileAccessories, sorting, PROFILE_ACCESSORIES_SORTING_MAPPINGS) if sorting else []
        
        # Apply filters and sorting if there are any, else get all records
        if filter_conditions:
            query = ProfileAccessories.query.filter(and_(*filter_conditions))
        else:
            query = ProfileAccessories.query
        
        # Apply sorting
        if sort_conditions:
            query = query.order_by(*sort_conditions)
    
        # Paginate the filtered query
        data = paginate_query(
            query=query,
            per_page=per_page,
            page=page,
            items_name="profile_accessories"
        )
        
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
