from math import ceil
from flask import request
from datetime import datetime
from sqlalchemy.sql import func
from typing import Optional, Tuple, Dict, Any, List, Callable
from sqlalchemy.orm.query import Query
from app.types.consts import (
    PAGE_PARAM,
    PER_PAGE_PARAM
)
from app.types.length import (
    PAGE,
    PER_PAGE,
    PER_PAGE_LIMIT,
    PAGE_LIMIT
)

def record_exists(model, **kwargs) -> bool:
    """
    Check if a record exists in the database based on the provided filter criteria.

    :param model: SQLAlchemy model class.
    :param kwargs: Filter criteria.
    :return: True if the record exists, False otherwise.
    """
    return model.query.filter_by(**kwargs).first() is not None

def get_filter_params() -> Dict[str, Any]:
    """
    Helper function to get filter parameters from the request body.

    :return: Dictionary containing filter parameters and their values.
    """
    filters = {}

    # Iterate through the request body parameters
    if request.json and 'filter' in request.json:
        for filter_item in request.json['filter']:
            for key, value in filter_item.items():
                    filters[key] = value
    return filters

def get_sort_params():
    """
    Helper function to get sort parameters from the request body.

    :return: Dictionary containing sort parameters and their values.
    """
    sort_parms = {}

    # Check if the request body contains the "sort" object
    if request.json and 'sort' in request.json:
        for sort_item in request.json['sort']:
            for key, value in sort_item.items():
                sort_parms[key] = value
    return sort_parms

def get_creation_params(force: bool = False) -> Dict[str, Any]:
    """
    Helper function to get creation parameters from the request body.

    :param force: If True, raise an error if the "creation" object is not found in the request body.
    :return: Dictionary containing creation parameters and their values.
    :raises ValueError: If force is True and "creation" object is not found in the request body.
    """
    creation_params = {}

    # Check if the request body contains the "creation" object
    if request.json and 'creation' in request.json:
        for key, value in request.json['creation'].items():
            creation_params[key] = value
    elif force:
        raise ValueError("The 'creation' object is required in the request body.")
    return creation_params

def get_update_params(force: bool = False) -> Dict[str, Any]:
    """
    Helper function to get update parameters from the request body.

    :param force: If True, raise an error if the "update" object is not found in the request body.
    :return: Dictionary containing update parameters and their values.
    :raises ValueError: If force is True and "update" object is not found in the request body.
    """
    update_params = {}

    # Check if the request body contains the "update" object
    if request.json and 'update' in request.json:
        for key, value in request.json['update'].items():
            update_params[key] = value
    elif force:
        raise ValueError("The 'update' object is required in the request body.")
    return update_params

def get_pagination_params() -> Tuple[int, int]:
    """
    Helper function to get pagination parameters from the request query string.

    :return: Tuple with page number and number of items per page.
    """
    # limit the number of pages to PAGE_LIMIT
    page = min(request.args.get(PAGE_PARAM, PAGE, type=int), PAGE_LIMIT)
    print(page)

    # Limit the number of items per page to PER_PAGE_MAX
    per_page = min(request.args.get(PER_PAGE_PARAM, PER_PAGE, type=int), PER_PAGE_LIMIT)

    # Return page number and number of items per page
    return page, per_page

def paginate_query(
    query: Query,
    page: int = PAGE,
    per_page: int = PER_PAGE,
    items_name: str = 'items',
    to_representation: Optional[Callable] = None
) -> Dict[str, Any]:
    """
    Helper function to paginate a SQLAlchemy query.

    :param query: SQLAlchemy query object.
    :param page: Current page number. Defaults to 1.
    :param per_page: Number of items per page. Defaults to 20.
    :param items_name: Key for the items in the response. Defaults to 'items'.
    :param to_representation: Function to represent the object. Defaults to None (to_dict method will be used).
    :return: Dictionary with paginated results and metadata.
    """
    # Total number of items
    total = query.count()
    
    # Calculate the number of pages
    total_pages = ceil(total / per_page)

    # Apply limit and offset to the query for pagination
    items = query.limit(per_page).offset((page - 1) * per_page).all()

    # Use the specified function or fallback to to_dict if not provided
    if to_representation is None:
        to_representation = lambda obj: obj.to_dict()

    # Return paginated data and metadata
    return {
        items_name: [to_representation(i) for i in items],  # Paginated items
        "_meta" : {
            'total': total,               # Total number of items
            'pages': total_pages,         # Total number of pages
            'current_page': page,         # Current page number
            'next_page': page + 1 if page < total_pages else None,  # Next page number or None
            'prev_page': page - 1 if page > 1 else None  # Previous page number or None
        }
    }

def build_sort_conditions(
    model,
    sort_params: Dict[str, str] = {},
    sort_mapping: Dict[str, str] = {}
) -> List:
    """
    Build SQLAlchemy sort conditions based on provided sort parameters and sort mapping.

    :param model: SQLAlchemy model class.
    :param sort_params: Dictionary of sort parameters with field names as keys and sort directions as values.
    :param sort_mapping: Dictionary mapping sort field names to model column names.
                         Example: {'name': 'accessory_name'}
    :return: List of SQLAlchemy sort conditions.
    """
    sort_conditions = []

    for field, direction in sort_params.items():
        # Check if the field is in sort_mapping
        if field in sort_mapping:
            # Get the model column
            column_name = sort_mapping[field]
            column = getattr(model, column_name, None)

            if column is None:
                continue  # Skip if the column does not exist

            # Apply the appropriate sort condition based on the sort direction
            if direction == 'asc':
                sort_conditions.append(column.asc())
            elif direction == 'desc':
                sort_conditions.append(column.desc())
    return sort_conditions

def build_filter_conditions(
    model,
    filters: Dict[str, Any] = {},
    filter_mapping: Dict[str, Dict[str, str]] = {}
) -> List:
    """
    Build SQLAlchemy filter conditions based on provided filters and filter mapping.

    :param model: SQLAlchemy model class.
    :param filters: Dictionary of filters with field names as keys.
    :param filter_mapping: Dictionary mapping filter field names to model column names and filter types.
                           Example: {'name': {'field': 'accessory_name', 'type': 'like'}}
    :return: List of SQLAlchemy filter conditions.
    """
    filter_conditions = []

    for field, value in filters.items():
        # Check if the field is in filter_mapping
        if field in filter_mapping:
            # Get the model column and filter type
            column_name = filter_mapping[field]['field']
            filter_type = filter_mapping[field].get('type', 'exact')  # Default to 'exact' if not specified
            column = getattr(model, column_name, None)

            if column is None:
                continue  # Skip if the column does not exist

            # Apply the appropriate filter condition based on the filter type
            # Filter for 'like' type
            if filter_type == 'like':
                filter_conditions.append(column.like(f"%{value}%"))

            # Filter for 'number' type
            elif filter_type == 'number':
                if "exact" in value:
                    filter_conditions.append(column == value['exact'])
                if "gt" in value:
                    filter_conditions.append(column > value['gt'])
                if "gte" in value:
                    filter_conditions.append(column >= value['gte'])
                if "lt" in value:
                    filter_conditions.append(column < value['lt'])
                if "lte" in value:
                    filter_conditions.append(column <= value['lte'])
                if "range" in value:
                    filter_conditions.append(column.between(value['range'][0], value['range'][1]))

            # Filter for 'date' type
            elif filter_type == 'date' and isinstance(value, dict):
                # Handle date filters for 'created_at'
                if 'exact' in value:
                    exact_date = datetime.fromisoformat(value['exact']).date()
                    filter_conditions.append(func.date(column) == exact_date)
                if 'before' in value:
                    before_date = datetime.fromisoformat(value['before']).date()
                    filter_conditions.append(func.date(column) < before_date)
                if 'before-inc' in value:
                    before_date = datetime.fromisoformat(value['before-inclusive']).date()
                    filter_conditions.append(func.date(column) <= before_date)
                if 'after' in value:
                    after_date = datetime.fromisoformat(value['after']).date()
                    filter_conditions.append(func.date(column) > after_date)
                if 'after-inc' in value:
                    after_date = datetime.fromisoformat(value['after-inclusive']).date()
                    filter_conditions.append(func.date(column) >= after_date)
            else:
                # Default to exact match for fields with 'exact' type or unspecified type
                filter_conditions.append(column == value)
    return filter_conditions

def build_update_params(
    record,
    update_params: Dict[str, Any] = {},
    update_mapping: Dict[str, str] = {}
) -> None:
    """
    Build update parameters based on provided update parameters and update mapping.

    :param record: SQLAlchemy record object to update.
    :param update_params: Dictionary of update parameters with field names as keys.
    :param update_mapping: Dictionary mapping update field names to model column names.
                           Example: {'name': 'accessory_name'}
    """
    for field, value in update_params.items():
        # Check if the field is in update_mapping
        if field in update_mapping:
            # Get the model column
            column_name = update_mapping[field]
            column = getattr(record, column_name, None)

            if column is None:
                continue  # Skip if the column does not exist

            # Update the record attribute with the new value
            setattr(record, column_name, value)
    return None
