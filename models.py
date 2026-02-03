from extensions import db
from datetime import datetime,timezone,timedelta

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(20))
    points = db.Column(db.Integer)
    badge = db.Column(db.String(50))
    location = db.Column(db.String(100))
    dob = db.Column(db.Date)         
    mobile = db.Column(db.String(15))
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime)

class Otp(db.Model):
    __tablename__ = "otp"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False
    )

    otp_code = db.Column(db.String(6), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime,default=lambda: datetime.now(timezone.utc))

    