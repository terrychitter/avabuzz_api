from math import ceil
from flask import request
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import aliased
from sqlalchemy.orm.attributes import InstrumentedAttribute
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
    sort_mapping: Dict[str, str] = {},
) -> List:
    """
    Build SQLAlchemy sort conditions based on provided sort parameters and sort mapping.
    Supports sorting on nested relationships.

    :param model: SQLAlchemy model class.
    :param sort_params: Dictionary of sort parameters with field names as keys and sort directions as values.
                        Example: {'field_name': 'asc'}
    :param sort_mapping: Dictionary mapping sort field names to model column names or paths.
                         Example: {'name': 'relation.column_name'}
    :return: List of SQLAlchemy sort conditions.
    """
    sort_conditions = []

    def get_nested_column(model, path: str):
        """
        Recursively resolve nested relationships and return the column.
        Example: "relation1.relation2.column"
        """
        parts = path.split(".")
        current_model = model
        for part in parts[:-1]:  # Traverse relationships
            relationship = getattr(current_model, part, None)
            if relationship is None:
                return None  # Invalid path
            current_model = relationship.property.mapper.class_
        # Get the final column
        return getattr(current_model, parts[-1], None)

    for field, direction in sort_params.items():
        # Check if the field is in sort_mapping
        if field in sort_mapping:
            # Get the column path
            column_path = sort_mapping[field]
            column = get_nested_column(model, column_path)

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
    filter_mapping: Dict[str, Dict[str, str]] = {},
) -> List:
    filter_conditions = []

    def get_nested_column(model, path: str):
        """
        Recursively resolve nested relationships and return the column.
        Example: "relation1.relation2.column"
        """
        parts = path.split(".")
        current_model = model
        for part in parts[:-1]:  # Traverse relationships
            relationship = getattr(current_model, part, None)
            if relationship is None:
                return None  # Invalid path
            current_model = relationship.property.mapper.class_
        # Get the final column
        return getattr(current_model, parts[-1], None)

    def parse_date(date_str: str) -> datetime:
        """
        Parses a date string and raises a ValueError if the format is invalid.
        """
        try:
            return datetime.fromisoformat(date_str)
        except ValueError:
            raise ValueError(f"Invalid date format: {date_str}. Expected ISO format (YYYY-MM-DD).")

    # Loop through filters and build conditions
    for field, value in filters.items():
        if field in filter_mapping:
            mapping = filter_mapping[field]
            column_path = mapping['field']
            filter_type = mapping.get('type', 'exact')

            # Get the column from the model or its relationships
            column = get_nested_column(model, column_path)
            if column is None:
                continue  # Skip if the column does not exist

            # Build condition based on filter type
            if filter_type == 'like':
                filter_conditions.append(column.ilike(f"%{value}%"))
            elif filter_type == 'exact':
                filter_conditions.append(column == value)
            elif filter_type == 'date':
                # Handle date-based filtering with operators
                if isinstance(value, dict):  # Check if multiple operators are specified
                    for op, date_value in value.items():
                        if isinstance(date_value, str):
                            date_value = parse_date(date_value)  # Validate and parse date
                        if op == "exact":
                            filter_conditions.append(column == date_value)
                        elif op == "gt":
                            filter_conditions.append(column > date_value)
                        elif op == "gte":
                            filter_conditions.append(column >= date_value)
                        elif op == "lt":
                            filter_conditions.append(column < date_value)
                        elif op == "lte":
                            filter_conditions.append(column <= date_value)
                        else:
                            raise ValueError(f"Unsupported date operator: {op}")
                else:
                    # Default to exact match for non-dict values
                    date_value = parse_date(value)  # Validate and parse date
                    filter_conditions.append(column == date_value)

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
