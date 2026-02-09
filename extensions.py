from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

# db is a single shared database object that the whole project uses

db = SQLAlchemy()
mail = Mail()