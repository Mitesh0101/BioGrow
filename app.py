import random
from flask import Flask, redirect, request, url_for, render_template, session
from config import Config
from extensions import db, mail
from datetime import datetime, timedelta
from models import User, Otp
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from chatbot import chatbot_bp

app = Flask(__name__)

app.register_blueprint(chatbot_bp)

# App config
app.config.from_object(Config)
db.init_app(app)
mail.init_app(app)

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


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    if not user.is_verified:
        return redirect(url_for("verify_otp", user_id=user.user_id))

    return render_template("Dashboard/dashboard.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ================= OTP VERIFY =================
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


# ================= RESEND OTP =================
@app.route("/resend-otp/<int:user_id>")
def resend_otp(user_id):
    user = User.query.get(user_id)

    if not user:
        return "Invalid user"

    if user.is_verified:
        return redirect(url_for("login"))

    # Invalidate old OTPs
    Otp.query.filter_by(user_id=user_id, is_used=False).update(
        {"is_used": True}
    )

    # Generate new OTP
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


# ================= REGISTER =================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")
        location = request.form.get("location")
        dob_str = request.form.get("dob")
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
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
            is_verified=False,
            created_at=datetime.utcnow()
        )

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

@app.route("/crop_prediction")
def crop_prediction():
    return render_template("Crop_Prediction/crop_prediction.html")


@app.route("/farmer_community")
def farmer_community():
    return render_template("Farmer_Community/farmer_community.html")


@app.route("/profile")
def profile():
    return render_template("Profile/profile.html")


# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
