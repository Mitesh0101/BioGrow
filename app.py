import random   # Used to generate OTP
from datetime import datetime, timedelta
import os   # Used to get env
import requests     # Used to fetch from weather API
from flask import Flask, redirect, request, url_for, render_template, session,flash
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv  # Used to load environment variables

from utils.email import send_otp_email
from auth import auth_bp
from community import community_bp, give_daily_bonus

# ================= ENV =================
load_dotenv()

# ================= CONFIG & EXTENSIONS =================
from config import Config
from extensions import db, mail

# ================= APP INIT =================
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
mail.init_app(app)

# ================= MODELS =================
from models import User, Otp,Answer,Topic

# ================= BLUEPRINTS =================
from chatbot import chatbot_bp
from crop_prediction import crop_prediction_bp
from crop_tracking import crop_tracking_bp

app.register_blueprint(chatbot_bp)
app.register_blueprint(crop_prediction_bp)
app.register_blueprint(crop_tracking_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(community_bp)

from utils.avtar import get_initials

# ================= ROUTES =================
@app.route("/")
def home():
    return render_template("HomePage/home_page.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    now = datetime.now()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = User.query.filter_by(email=email).first()

        # check_password_hash() is a function of werkzeug.security for security of password
        # check_password_hash(hashed password stored in db during register,plain password entered by user)
        if user and check_password_hash(user.password_hash, password):
            # if user is doing login for the first time then he will have to get verified using otp
            if not user.is_verified:
                Otp.query.filter_by(
                    user_id = user.user_id,
                    is_used = False
                ).update({"is_used":True})


                generated_otp = str(random.randint(100000, 999999))
                otp = Otp(
                    user_id=user.user_id,
                    otp_code=generated_otp,
                    expires_at=now + timedelta(minutes=10),
                    is_used = False
                )
                db.session.add(otp)
                db.session.commit()


                send_otp_email(user.email,generated_otp,user.full_name)
                return redirect(url_for("verify_otp", user_id=user.user_id))
            session["user_id"] = user.user_id
            session["full_name"] = user.full_name
            session["initials"] = get_initials(user.full_name)
            session["location"] = user.location
            give_daily_bonus(user.user_id)
            
            return redirect(url_for("dashboard"))

        flash("Invalid email or Password","danger")
        return redirect(url_for('login'))

    return render_template("Login/login.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_record = User.query.get(session["user_id"])

    if not user_record.is_verified:
        return redirect(url_for("verify_otp", user_id=user_record.user_id))

    # 🌤 WEATHER LOGIC
    api_key = os.getenv("WEATHER_API")
    city = user_record.location

    weather_data = None

    if api_key and city:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={api_key}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            weather_data = {
                "temp": data["main"]["temp"],
                "description": data["weather"][0]["description"]
            }

    return render_template(
        "Dashboard/dashboard.html",
        user=user_record,
        weather=weather_data
    )

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ---------------- OTP VERIFY ----------------
@app.route("/verify-otp/<int:user_id>", methods=["GET", "POST"])
def verify_otp(user_id):
    if request.method == "POST":
        entered_otp = request.form.get("otp").strip()
        now = datetime.now()

        otp_record = (
            Otp.query
            .filter(
                Otp.user_id == user_id,
                Otp.is_used == False
            )
            .order_by(Otp.created_at.desc())
            .first()
        )

        if not otp_record or otp_record.otp_code != entered_otp:
            return render_template(
                "Otp/verify_otp.html",
                error="Invalid OTP",
                user_id=user_id
            )

        if otp_record.expires_at < now:
            return render_template(
                "Otp/verify_otp.html",
                error="OTP Expired",
                user_id=user_id
            )

        otp_record.is_used = True
        user = User.query.get(user_id)
        user.is_verified = True
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("Otp/verify_otp.html", user_id=user_id)

# ---------------- RESEND OTP ----------------
@app.route("/resend-otp/<int:user_id>")
def resend_otp(user_id):
    user = User.query.get(user_id)
    
    if not user:
        return "Invalid user"
    
    if user.is_verified:
        return redirect(url_for("login"))

    Otp.query.filter_by(user_id=user_id, is_used=False).update(
        {"is_used": True}
    )

    now = datetime.now()
    new_otp = str(random.randint(100000, 999999))
    otp = Otp(
        user_id=user_id,
        otp_code=new_otp,
        expires_at=now + timedelta(minutes=10),
        is_used = False
    )

    db.session.add(otp)
    db.session.commit()

    send_otp_email(user.email, new_otp,user.full_name)
    return redirect(url_for("verify_otp", user_id=user_id))

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = User(
            full_name=request.form.get("full_name"),
            email=request.form.get("email"),
            password_hash=generate_password_hash(request.form.get("password")),
            role="FARMER",
            points=0,
            location=request.form.get("location"),
            dob=datetime.strptime(request.form.get("dob"), "%Y-%m-%d").date(),
            mobile=request.form.get("mobile"),
            is_verified=False,
            created_at=datetime.now()
        )

        if User.query.filter_by(email=user.email).first():
            return "Email already registered"

        db.session.add(user)
        db.session.commit()

        otp_code = str(random.randint(100000, 999999))
        otp = Otp(
            user_id=user.user_id,
            otp_code=otp_code,
            expires_at=datetime.now() + timedelta(minutes=10),
            is_used = False
        )

        db.session.add(otp)
        db.session.commit()

        send_otp_email(user.email, otp_code,user.full_name)
        return redirect(url_for("verify_otp", user_id=user.user_id))
    
    return render_template("Login/login.html")

BADGE_ORDER = [
    ("Beginner", 0),
    ("Contributor", 50),
    ("Trusted Farmer", 150),
    ("Expert Farmer", 300),
]

def get_next_badge_info(lifetime_points):
    for badge, points in BADGE_ORDER:
        if lifetime_points < points:
            return badge, points
    return "Max Level", None


@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    user = User.query.get(session["user_id"])
    question_count = Topic.query.filter_by(user_id = user.user_id).count()
    answers_count = Answer.query.filter_by(user_id=user.user_id).count()
    best_answers_count = Answer.query.filter_by(
        user_id=user.user_id,
        is_best_solution=True
    ).count()
    next_badge, next_badge_points = get_next_badge_info(user.lifetime_points)

    return render_template("Profile/profile.html",user=user,question_count=question_count,answers_count=answers_count,best_answers_count=best_answers_count,next_badge=next_badge,next_badge_points=next_badge_points)

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)