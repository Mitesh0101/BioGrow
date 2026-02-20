from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

# It is created, but not connected to Flask app yet.

db = SQLAlchemy()
mail = Mail()