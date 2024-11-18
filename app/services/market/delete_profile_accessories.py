from app import db
from flask import jsonify, Response
from typing import Tuple
from app.utils.io import record_exists
from app.models import ProfileAccessories

def delete_profile_accessories(item_id: str) -> Tuple[Response, int]:
    try:
        # Check if the item exists
        if not record_exists(ProfileAccessories, accessory_id=item_id):
            return jsonify({"error": "Item not found"}), 404
        
        # Delete the item
        db.session.query(ProfileAccessories).filter(ProfileAccessories.accessory_id == item_id).delete() # type: ignore

        db.session.commit()

        return jsonify({"message": "Item deleted successfully"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500