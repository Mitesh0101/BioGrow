from flask import Flask, redirect, request, url_for, Response, render_template,session

# Config means database config (username, password, db name)
from config import Config

# db is SQLAlchemy database object
from extensions import db
from datetime import datetime

# User is table imported from models
from models import User

# To Secure Password
from werkzeug.security import generate_password_hash, check_password_hash

# Import chatbot blueprint
from chatbot import chatbot_bp

# app → your website
app = Flask(__name__)

# Add chatbot blueprint
app.register_blueprint(chatbot_bp)

# Connect Flask app with database
app.config.from_object(Config)
db.init_app(app)


@app.route("/")
def home():
    return render_template("HomePage/home_page.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # User => database table
        # User.query => asking some data from User Table
        # User.query.filter_by(email=email) => select * from user WHERE email=input_email;
        # .first() match the first record
        user = User.query.filter_by(email=email).first()

        # check_password_hash is method of library werkzeug.security which compares hashed password stored in db table and password enterd by user
        if user and check_password_hash(user.password_hash, password):
            # Save user info in session
            session["user_id"] = user.user_id
            session["full_name"] = user.full_name
            return redirect(url_for("dashboard"))
        else:
            return "Invalid email or password"

    return render_template("Login/login.html")



@app.route("/profile")
def profile():
    return render_template("Profile/profile.html")


@app.route("/dashboard")
def dashboard():
    # If user not logged in then redirect to login
    if "user_id" not in session:
        return redirect(url_for("login"))
    # If logged in then show dashboard
    return render_template("Dashboard/dashboard.html")


@app.route("/crop_prediction")
def crop_prediction():
    return render_template("Crop_Prediction/crop_prediction.html")


@app.route("/farmer_community")
def farmer_community():
    return render_template("Farmer_Community/farmer_community.html")

# Clears session (Logout User)
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")
        location = request.form.get("location")
        dob = request.form.get("dob")
        mobile = request.form.get("mobile")

        if User.query.filter_by(email=email).first():
            return "Email already registered"

        user = User(
            full_name=full_name,
            email=email,
            password_hash=generate_password_hash(password),
            role="FARMER",
            badge="Beginner",
            points=0,
            location=location,
            dob=dob,
            mobile=mobile,
            created_at=datetime.now()
        )

        # Add User in db table
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for("login"))
    return render_template("Login/login.html")

if __name__ == "__main__":
    app.run(debug=True)
