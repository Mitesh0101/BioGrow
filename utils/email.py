from flask_mail import Message
from flask import current_app
from extensions import mail

def send_otp_email(to_email, otp, full_name):
    msg = Message(
        subject="Your BioGrow Verification Code 🌱",
        sender=("BioGrow", current_app.config["MAIL_USERNAME"]),
        recipients=[to_email]
    )

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <body style="margin:0;padding:0;background-color:#f4f6f9;font-family:Arial,sans-serif;">

    <table align="center" width="100%" cellpadding="0" cellspacing="0" 
           style="max-width:600px;background:white;margin-top:40px;
           border-radius:10px;overflow:hidden;box-shadow:0 6px 20px rgba(0,0,0,0.1);">

        <!-- Header -->
        <tr>
            <td style="background:linear-gradient(135deg,#2ecc71,#27ae60);
                       padding:30px;text-align:center;color:white;">
                <h1 style="margin:0;">🌱 BioGrow</h1>
                <p style="margin:5px 0 0 0;">Empowering Farmers with Smart Technology</p>
            </td>
        </tr>

        <!-- Body -->
        <tr>
            <td style="padding:30px;color:#333;">
                <h2>Hello {full_name},</h2>
                <p style="font-size:16px;line-height:1.6;">
                    Welcome to BioGrow 🌾 We're excited to have you in our farmer community.
                </p>

                <p style="font-size:16px;">
                    Please use the verification code below:
                </p>

                <!-- OTP BOX -->
                <div style="background:#f1fdf6;
                            border:2px dashed #27ae60;
                            padding:20px;
                            text-align:center;
                            font-size:28px;
                            font-weight:bold;
                            letter-spacing:5px;
                            color:#27ae60;
                            border-radius:8px;
                            margin:20px 0;">
                    {otp}
                </div>

                <p style="font-size:14px;color:#777;">
                    ⏳ This OTP is valid for 10 minutes.<br>
                    🔒 Do not share this code with anyone.
                </p>

                <p style="font-size:14px;color:#777;">
                    If you did not request this verification, you can safely ignore this email.
                </p>
            </td>
        </tr>

        <!-- Footer -->
        <tr>
            <td style="background:#f8f9fa;padding:20px;text-align:center;
                       font-size:12px;color:#888;">
                © 2026 BioGrow | All Rights Reserved<br>
                This is an automated email. Please do not reply.
            </td>
        </tr>

    </table>

    </body>
    </html>
    """

    msg.html = html_content
    mail.send(msg)
