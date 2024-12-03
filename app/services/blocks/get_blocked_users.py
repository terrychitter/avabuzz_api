from app import db
from typing import Any, Dict, Optional, Tuple
from flask import Response, jsonify
from app.models import Users, BlockedUsers
from app.utils.io import record_exists, paginate_query
from app.utils.io import PAGE, PER_PAGE, build_sort_conditions, build_filter_conditions
from app.types.mappings.filters import BLOCKED_USERS_FILTER_MAPPINGS
from app.types.mappings.sorting import BLOCKED_USERS_SORTING_MAPPINGS
from sqlalchemy.orm import aliased
from sqlalchemy.orm.collections import InstrumentedList

def get_blocked_users(
    private_user_id: str, 
    filters: Optional[Dict[str, Any]] = None, 
    page: int = PAGE, 
    per_page: int = PER_PAGE, 
    sorting: Optional[Dict[str, Any]] = None
) -> Tuple[Response, int]:
    try:
        # Check if the user exists
        if not record_exists(Users, private_user_id=private_user_id):
            return jsonify({"message": "User not found"}), 404
        
        # Build the filter conditions
        if filters:
            filter_conditions = build_filter_conditions(
                model=BlockedUsers,
                filters=filters,
                filter_mapping=BLOCKED_USERS_FILTER_MAPPINGS
            )

        # Build the sort conditions
        if sorting:
            sort_conditions = build_sort_conditions(
                model=BlockedUsers,
                sort_params=sorting,
                sort_mapping=BLOCKED_USERS_SORTING_MAPPINGS
            )


       # Query the database for blocked users with optional filters and sorting
        blocked_users_query = (
            db.session.query(BlockedUsers)
            .join(BlockedUsers.blocked)
            .filter(BlockedUsers.blocker_id == private_user_id) # type: ignore
            .filter(*filter_conditions if filters else [])
            .order_by(*sort_conditions if sorting else [])
)

        # Paginate the query
        pagination_result = paginate_query(
            query=blocked_users_query,
            page=page,
            per_page=per_page,
            items_name="blocked_users",
            to_representation=lambda blocked_user: blocked_user.to_dict([BlockedUsers.DictKeys.BLOCKER])
            )

        return jsonify(pagination_result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


