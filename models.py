from extensions import db

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

    created_at = db.Column(db.DateTime)

