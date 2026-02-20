import os
from dotenv import load_dotenv
# without this method python can not see .env variables
load_dotenv()

class Config:
    # This line gets database url from .env
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    
    # Disables unnecessary tracking (Saves Memory)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv("SECRET_KEY")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT"))
    
    # Sends Email Securly
    # Transport layer security
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

