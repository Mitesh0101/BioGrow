from flask import Flask, redirect, request, url_for, Response, render_template,session
from config import Config
from extensions import db
from datetime import datetime
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
app.secret_key = "Supersecret"
app.config.from_object(Config)
db.init_app(app)

@app.route("/")
def home():
    return render_template("HomePage/home_page.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
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
    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("Dashboard/dashboard.html")


@app.route("/crop_prediction")
def crop_prediction():
    return render_template("Crop_Prediction/crop_prediction.html")


@app.route("/farmer_community")
def farmer_community():
    return render_template("Farmer_Community/farmer_community.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form["full_name"]
        email = request.form["email"]
        password = request.form["password"]
        location = request.form["location"]
        dob = request.form["dob"]
        mobile = request.form["mobile"]

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


        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("Login/login.html")

print("DB =", app.config["SQLALCHEMY_DATABASE_URI"])


if __name__ == "__main__":
    app.run(debug=True)
