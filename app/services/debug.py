from datetime import datetime
from typing import Tuple
from flask import Response, jsonify
from app import db
from app.models import HashTags
from app.types.enum import ProfileAccessoryType, ProfileType, OwnershipType
from app.utils.id_generation import generate_uuid

def debug_service() -> Tuple[Response, int]:
    try:

        item = HashTags(
            hashtag_id=generate_uuid(),
            hashtag_name="helloworld",
            views=10,
            post_count=0
        )

        print(item)

        return jsonify({"message": "Debug Successful!", "item": item.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    