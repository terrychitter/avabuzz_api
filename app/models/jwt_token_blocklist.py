from app import db
import datetime


class JWTTokenBlocklist(db.Model):
    __tablename__ = "jwt_token_blocklist"

    jwt_token_blocklist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jti = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    def __repr__(self):
        return f"<Token {self.jti}>"
    

    
