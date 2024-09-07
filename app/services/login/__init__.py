from typing import Optional, Tuple
from flask import Response
from app.services.login.login import login

def login_service(login_data: dict) -> Tuple[Response, int]:
    return login(login_data)