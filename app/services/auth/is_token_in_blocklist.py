def is_token_in_blocklist(jti: str) -> bool:
    """
    Check if the token is in the blocklist

    Args:
        jti (str): The JWT ID of the token to check

    Returns:
        bool: True if the token is in the blocklist, False otherwise
    """
    from app.models import JWTTokenBlocklist
    token = JWTTokenBlocklist.query.filter_by(jti=jti).first()
    return token is not None