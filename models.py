from extensions import db
from datetime import datetime,timezone, date
from sqlalchemy.dialects.postgresql import JSONB  # Required for the flexible data


# ================= USER =================
class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)

    role = db.Column(db.String(20), default="FARMER")
    points = db.Column(db.Integer, default=0, nullable=False)
    badge = db.Column(db.String(50), default="Beginner", nullable=False)

    location = db.Column(db.String(100))
    dob = db.Column(db.Date)
    mobile = db.Column(db.String(10))
    is_verified = db.Column(db.Boolean, default=False)
    lifetime_points = db.Column(db.Integer, default=0, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now())


# ================= OTP =================
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

    created_at = db.Column(db.DateTime, default=datetime.now())


# ================= TOPIC =================
class Topic(db.Model):
    __tablename__ = "topics"

    topic_id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False
    )

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))

    is_pinned = db.Column(db.Boolean, default=False)
    pinned_until = db.Column(db.DateTime)

    created_at = db.Column(db.DateTime, default=datetime.now())

    user = db.relationship("User", backref="topics")


# ================= ANSWER =================
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
    has_earned_best_points = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.now())

    user = db.relationship("User")
    topic = db.relationship("Topic", backref="answers")
    
    comments = db.relationship(
        "AnswerComment",
        order_by="AnswerComment.created_at.asc()",
        cascade="all, delete-orphan"
    )

    likes = db.relationship(
        "AnswerLike",
        cascade="all, delete-orphan"
    )

class CropStandard(db.Model):
    __tablename__ = 'crop_standards'

    crop_standard_id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(50), unique=True, nullable=False)
    display_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    growth_config = db.Column(JSONB, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

class UserCrop(db.Model):
    __tablename__ = 'user_crops'

    user_crop_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    crop_standard_id = db.Column(db.Integer, db.ForeignKey('crop_standards.crop_standard_id'), nullable=False)
    farm_name = db.Column(db.String(100))
    sowing_date = db.Column(db.Date, nullable=False)
    area_acres = db.Column(db.Float, default=1.0)
    status = db.Column(db.String(20), default='active') # 'active', 'harvested'
    created_at = db.Column(db.DateTime, default=datetime.now())

    standard = db.relationship('CropStandard', backref='farms')

class CropLog(db.Model):
    __tablename__ = 'crop_logs'

    crop_log_id = db.Column(db.Integer, primary_key=True)
    user_crop_id = db.Column(db.Integer, db.ForeignKey('user_crops.user_crop_id', ondelete='CASCADE'), nullable=False)
    log_date = db.Column(db.Date, default=date.today(), nullable=False)
    week_number = db.Column(db.Integer, nullable=True) # Calculated in Python before saving
    soil_moisture = db.Column(db.String(20), nullable=True) 
    plant_height_cm = db.Column(db.Float, nullable=True) 
    lcc_score = db.Column(db.Integer, nullable=True) # 1-6 Scale
    phenology_stage = db.Column(db.String(50), nullable=True) 
    stand_count = db.Column(db.Integer, nullable=True) 

    # Relationship to access logs from the parent UserCrop
    # Usage: my_farm.logs (returns a list of all logs for that farm)
    crop = db.relationship('UserCrop', backref=db.backref('logs', cascade="all, delete-orphan"))



# ================= POINT TRANSACTION =================
class PointTransaction(db.Model):
    __tablename__ = "point_transactions"

    transaction_id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False
    )

    points = db.Column(db.Integer, nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # CREDIT / DEBIT
    reason = db.Column(db.String(100))

    created_at = db.Column(db.DateTime, default=datetime.now())

    user = db.relationship("User", backref="point_transactions")


# ================= ANSWER COMMENT =================
class AnswerComment(db.Model):
    __tablename__ = "answer_comments"

    comment_id = db.Column(db.Integer, primary_key=True)

    answer_id = db.Column(
        db.Integer,
        db.ForeignKey("answers.answer_id", ondelete="CASCADE"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False
    )

    comment_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    user = db.relationship("User")

class AnswerLike(db.Model):
    __tablename__ = "answer_likes"

    like_id = db.Column(db.Integer, primary_key=True)

    answer_id = db.Column(
        db.Integer,
        db.ForeignKey("answers.answer_id", ondelete="CASCADE"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False
    )

    created_at = db.Column(db.DateTime, default=datetime.now())

    __table_args__ = (
        db.UniqueConstraint("answer_id", "user_id", name="unique_answer_like"),
    )
