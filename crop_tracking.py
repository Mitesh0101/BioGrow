from flask import Blueprint, render_template, session
from models import UserCrop
from datetime import date

crop_tracking_bp = Blueprint("crop_tracking", __name__, template_folder="templates", static_folder="static")

@crop_tracking_bp.route("/crop_tracking")
def crop_tracking():
    farms = UserCrop.query.filter_by(user_id=session["user_id"])
    return render_template("Crop_Tracking/crop_tracking.html", farms=farms, today=date.today())