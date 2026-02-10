import random
from datetime import datetime, timedelta

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash

from extensions import db
from models import User, Otp
from utils.email import send_otp_email


auth_bp = Blueprint("auth", __name__)
@auth_bp.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Email not registered","danger")
            return redirect(
                "Auth/forgot_password.html"
            )

        # invalidate old OTPs
        Otp.query.filter_by(
            user_id=user.user_id,
            is_used=False
        ).update({"is_used": True}) 

        generated_otp = str(random.randint(100000, 999999))
        otp = Otp(
            user_id=user.user_id,
            otp_code=generated_otp,
            expires_at=datetime.now() + timedelta(minutes=10),
            is_used=False
        )

        db.session.add(otp)
        db.session.commit()

        send_otp_email(user.email, generated_otp, user.full_name)
        flash("OTP sent to your email 📧", "info")
        return redirect(url_for("auth.reset_password_otp", user_id=user.user_id))

    return render_template("Auth/forgot_password.html")


@auth_bp.route("/reset_password_otp/<int:user_id>", methods=["GET", "POST"])
def reset_password_otp(user_id):
    if request.method == "POST":
        entered_otp = request.form.get("otp").strip()
        now = datetime.now()

        # 🔐 fetch ONLY latest unused OTP
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
                "Auth/reset_password_otp.html",
                error="Invalid OTP",
                user_id=user_id
            )

        if otp_record.expires_at < now:
            return render_template(
                "Auth/reset_password_otp.html",
                error="OTP Expired",
                user_id=user_id
            )

        otp_record.is_used = True
        db.session.commit()

        session["reset_allowed"] = True
        return redirect(url_for("auth.reset_password", user_id=user_id))

    return render_template("Auth/reset_password_otp.html", user_id=user_id)

@auth_bp.route("/reset_password/<int:user_id>", methods=["GET", "POST"])
def reset_password(user_id):

    if not session.get("reset_allowed"):
        return redirect(url_for("login"))

    if request.method == "POST":
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            return render_template(
                "Auth/reset_password.html",
                error="Passwords do not match",
                user_id=user_id
            )

        user = User.query.get(user_id)
        user.password_hash = generate_password_hash(password)
        db.session.commit()

        # cleanup
        session.pop("reset_allowed", None)

        flash("Password reset successful! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("Auth/reset_password.html", user_id=user_id)
