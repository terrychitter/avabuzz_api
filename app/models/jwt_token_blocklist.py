import datetime
from app import db
from app.utils.id_generation import generate_uuid


class JWTTokenBlocklist(db.Model): # type: ignore
    __tablename__ = "jwt_token_blocklist"

    jwt_token_blocklist_id = db.Column(db.Integer, primary_key=True, default=generate_uuid)
    jti = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    def __repr__(self):
        return f"<Token {self.jti}>"
    

    
