from extensions import db
from datetime import datetime,timezone
from sqlalchemy.dialects.postgresql import JSONB  # Required for the flexible data

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(20))
    points = db.Column(db.Integer)
    badge = db.Column(db.String(50),nullable=False, default="Beginner")
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

class Topic(db.Model):
    __tablename__ = "topics"
    
    topic_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))
    is_pinned = db.Column(db.Boolean, default=False)
    pinned_until = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="topics")

class Answer(db.Model):
    __tablename__ = "answers"

    answer_id = db.Column(db.Integer, primary_key=True)

    topic_id = db.Column(
        db.Integer,
        db.ForeignKey("topics.topic_id", ondelete="CASCADE"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False
    )

    answer_text = db.Column(db.Text, nullable=False)
    is_best_solution = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User")
    topic = db.relationship("Topic", backref="answers")

class CropStandard(db.Model):
    __tablename__ = 'crop_standards'

    crop_standard_id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(50), unique=True, nullable=False)
    display_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    growth_config = db.Column(JSONB, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserCrop(db.Model):
    __tablename__ = 'user_crops'

    user_crop_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    crop_standard_id = db.Column(db.Integer, db.ForeignKey('crop_standards.crop_standard_id'), nullable=False)
    farm_name = db.Column(db.String(100))
    sowing_date = db.Column(db.Date, nullable=False)
    area_acres = db.Column(db.Float, default=1.0)
    status = db.Column(db.String(20), default='active') # 'active', 'harvested'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    standard = db.relationship('CropStandard', backref='farms')

class CropLog(db.Model):
    __tablename__ = 'crop_logs'

    crop_log_id = db.Column(db.Integer, primary_key=True)
    user_crop_id = db.Column(db.Integer, db.ForeignKey('user_crops.user_crop_id', ondelete='CASCADE'), nullable=False)
    log_date = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    week_number = db.Column(db.Integer, nullable=True) # Calculated in Python before saving
    soil_moisture = db.Column(db.String(20), nullable=True) 
    plant_height_cm = db.Column(db.Float, nullable=True) 
    lcc_score = db.Column(db.Integer, nullable=True) # 1-6 Scale
    phenology_stage = db.Column(db.String(50), nullable=True) 
    stand_count = db.Column(db.Integer, nullable=True) 

    # Relationship to access logs from the parent UserCrop
    # Usage: my_farm.logs (returns a list of all logs for that farm)
    crop = db.relationship('UserCrop', backref=db.backref('logs', cascade="all, delete-orphan"))