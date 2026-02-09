from flask_mail import Message
from flask import current_app
from extensions import mail

def send_otp_email(to_email, otp,full_name):
    msg = Message(
        subject="Your BioGrow Verification Code 🌱",
        # BioGrow is name and MAIL_USERNAME is sender email which came from config or env
        sender=("BioGrow", current_app.config["MAIL_USERNAME"]),
        recipients=[to_email]
    )
    msg.body = f"""
    Hello {full_name},
    Welcome to BioGrow 🌾
    We're excited to have you as part of our farmer community!
    To complete your verification, please use the One-Time Password (OTP) below:

    ━━━━━━━━━━━━━━━━━━━━
    🔐 Your OTP Code: {otp}
    ━━━━━━━━━━━━━━━━━━━━
    
    ⏳ This OTP is valid for 10 minutes.
    🔒 For your security, please do not share this code with anyone.

    If you did not request this verification, you can safely ignore this email.

    Warm regards,
    Team BioGrow
    🌱 Empowering Farmers with Smart Technology

    This is an automated message. Please do not reply.
"""
    mail.send(msg)
