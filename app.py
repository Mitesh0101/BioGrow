import random
import json
from datetime import datetime, timedelta

from flask import Flask, redirect, request, url_for, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from dotenv import load_dotenv

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
from models import User, Otp, Topic, Answer

with app.app_context():
    db.create_all()

# ================= BLUEPRINTS =================
from chatbot import chatbot_bp
from crop_prediction import crop_prediction_bp

app.register_blueprint(chatbot_bp)
app.register_blueprint(crop_prediction_bp)

# ================= AI VALIDATOR =================
from utils.answer_validator import validate_answer_with_ai

# ================= EMAIL FUNCTION =================
def send_otp_email(to_email, otp):
    msg = Message(
        subject="BioGrow Email Verification OTP",
        sender=("BioGrow", app.config["MAIL_USERNAME"]),
        recipients=[to_email]
    )
    msg.body = f"""
Your BioGrow OTP is: {otp}

This OTP is valid for 10 minutes.
Do not share this OTP with anyone.
"""
    mail.send(msg)

# ================= ROUTES =================
@app.route("/")
def home():
    return render_template("HomePage/home_page.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            if not user.is_verified:
                return redirect(url_for("verify_otp", user_id=user.user_id))

            session["user_id"] = user.user_id
            session["full_name"] = user.full_name
            return redirect(url_for("dashboard"))

        return "Invalid email or password"

    return render_template("Login/login.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])
    if not user.is_verified:
        return redirect(url_for("verify_otp", user_id=user.user_id))

    return render_template("Dashboard/dashboard.html")

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

        otp_record = Otp.query.filter_by(
            user_id=user_id,
            otp_code=entered_otp,
            is_used=False
        ).first()

        if not otp_record:
            return render_template(
                "Otp/verify_otp.html",
                error="Invalid OTP",
                user_id=user_id
            )

        if otp_record.expires_at < datetime.utcnow():
            return render_template(
                "Otp/verify_otp.html",
                error="OTP expired. Please resend OTP.",
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

    new_otp = str(random.randint(100000, 999999))
    otp = Otp(
        user_id=user_id,
        otp_code=new_otp,
        expires_at=datetime.utcnow() + timedelta(minutes=10)
    )

    db.session.add(otp)
    db.session.commit()

    send_otp_email(user.email, new_otp)
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
            created_at=datetime.utcnow()
        )

        if User.query.filter_by(email=user.email).first():
            return "Email already registered"

        db.session.add(user)
        db.session.commit()

        otp_code = str(random.randint(100000, 999999))
        otp = Otp(
            user_id=user.user_id,
            otp_code=otp_code,
            expires_at=datetime.utcnow() + timedelta(minutes=10)
        )

        db.session.add(otp)
        db.session.commit()

        send_otp_email(user.email, otp_code)
        return redirect(url_for("verify_otp", user_id=user.user_id))

    return render_template("Login/login.html")

# ---------------- FARMER COMMUNITY ----------------
@app.route("/farmer_community", methods=["GET", "POST"])
def farmer_community():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        topic = Topic(
            user_id=session["user_id"],
            title=request.form.get("title"),
            description=request.form.get("description"),
            category=request.form.get("category")
        )
        db.session.add(topic)
        db.session.commit()
        return redirect(url_for("farmer_community"))

    topics = Topic.query.order_by(
        Topic.is_pinned.desc(),
        Topic.created_at.desc()
    ).all()

    return render_template("Farmer_Community/farmer_community.html", topics=topics)

# ---------------- VIEW TOPIC ----------------
@app.route("/topic/<int:topic_id>", methods=["GET", "POST"])
def view_topic(topic_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    topic = Topic.query.get_or_404(topic_id)

    if request.method == "POST":
        answer = Answer(
            topic_id=topic_id,
            user_id=session["user_id"],
            answer_text=request.form.get("answer_text")
        )
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for("view_topic", topic_id=topic_id))

    return render_template("Farmer_Community/topic_detail.html", topic=topic)

# ---------------- MARK BEST ANSWER (AI SAFE) ----------------
@app.route("/mark-best/<int:answer_id>")
def mark_best_answer(answer_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    answer = Answer.query.get_or_404(answer_id)
    topic = db.session.get(Topic,answer.topic_id)

    if topic.user_id != session["user_id"]:
        return "Unauthorized", 403

    # 🔥 SAFE AI CALL
    try:
        ai_response = validate_answer_with_ai(
            topic.title + ". " + topic.description,
            answer.answer_text
        )
        ai_result = json.loads(ai_response)
    except Exception as e:
        print("AI ERROR:", e)
        ai_result = {
            "is_valid": True,
            "confidence": 50,
            "reason": "AI unavailable – fallback approval"
        }

    if ai_result["is_valid"] and ai_result["confidence"] >= 60:
        Answer.query.filter_by(
            topic_id=topic.topic_id,
            is_best_solution=True
        ).update({"is_best_solution": False})

        answer.is_best_solution = True
        db.session.commit()
        return redirect(url_for("view_topic", topic_id=topic.topic_id))

    return f"AI rejected answer: {ai_result['reason']}"

@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    user = User.query.get(session["user_id"])
    return render_template("Profile/profile.html",user=user)

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
