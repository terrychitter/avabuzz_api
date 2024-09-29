from typing import Type, Dict, Optional, Any
from sqlalchemy.orm import Query
from sqlalchemy.exc import SQLAlchemyError
from app import db

def value_exists(table, field_name: str, value: str, exclude_record: Optional[Dict[str, Any]] = None) -> bool:
    """
    Check if a given value exists in a specified field of a SQLAlchemy model table, optionally excluding specific records.

    Parameters:
    - table (Type[db.Model]): The SQLAlchemy model class representing the table to query.
    - field_name (str): The name of the field to check in the table.
    - value (str): The value to check for existence in the specified field.
    - exclude_record (Optional[Dict[str, any]]): A dictionary where keys are field names and values are the values to exclude. If None, no records are excluded.

    Returns:
    - bool: True if the value exists in the specified field of the table (excluding records matching the exclude criteria), False otherwise.

    Raises:
    - ValueError: If the provided table is not a valid SQLAlchemy model or if the field does not exist.
    - RuntimeError: If a database error occurs during the query execution.
    """
    try:
        # Ensure the table is a SQLAlchemy model
        if not issubclass(table, db.Model):
            raise ValueError("Provided table is not a valid SQLAlchemy model")

        # Build the query to check if the value exists in the specified field
        field = getattr(table, field_name, None)
        if field is None:
            raise ValueError(f"Field '{field_name}' does not exist on table '{table.__tablename__}'")

        query: Query = db.session.query(table).filter(field == value)

        if exclude_record:
            # Apply filters to exclude records based on provided criteria
            for ex_field_name, ex_value in exclude_record.items():
                ex_field = getattr(table, ex_field_name, None)
                if ex_field is None:
                    raise ValueError(f"Field '{ex_field_name}' does not exist on table '{table.__tablename__}'")
                query = query.filter(ex_field != ex_value)

        exists = query.first() is not None

        return exists
    
    except SQLAlchemyError as e:
        # Handle SQLAlchemy errors
        db.session.rollback()
        raise RuntimeError(f"Database error occurred: {str(e)}")

    except AttributeError:
        # Handle case where the field name does not exist on the model
        raise ValueError(f"Field '{field_name}' does not exist on table '{table.__tablename__}'")
