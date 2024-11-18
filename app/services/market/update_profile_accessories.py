from app import db
from flask import Response, jsonify
from typing import Any, Dict, Tuple
from app.models import ProfileAccessories
from app.utils.io import build_update_params
from app.types.mappings.update import PROFILE_ACCESSORIES_UPDATE_MAPPINGS

def update_profile_accessories(item_id: str, update_obj: Dict[str, Any]) -> Tuple[Response, int]:
    """
    Update a profile accessory.

    :param item_id: Profile accessory ID.
    :param update_obj: Dictionary with update parameters.
    :return: Tuple with response and status code.
    """
    try:
        # Retrieve the existing profile accessory
        accessory = db.session.query(ProfileAccessories).filter_by(accessory_id=item_id).first()

        if not accessory:
            return jsonify({"error": "Profile accessory not found"}), 404

        # Build the update parameters
        build_update_params(record=accessory, update_params=update_obj, update_mapping=PROFILE_ACCESSORIES_UPDATE_MAPPINGS)

        # Commit the changes, which will invoke validation
        db.session.commit()

        # Return the updated profile accessory
        new_accessory = db.session.query(ProfileAccessories).filter_by(accessory_id=item_id).first()
        if new_accessory:
            return jsonify({"message": f"Successfully updated profile accessory", "item": new_accessory.to_dict()}), 200
        else:
            return jsonify({"error": "Failed to retrieve updated profile accessory"}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
