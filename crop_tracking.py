from flask import Blueprint, render_template, session, jsonify, request, flash, redirect, url_for
from models import UserCrop, CropLog, CropStandard
from extensions import db
from datetime import date, datetime
import matplotlib
matplotlib.use('Agg') # Prevents matplotlib from opening plots on the server
import matplotlib.pyplot as plt
import io
import base64

crop_tracking_bp = Blueprint("crop_tracking", __name__, template_folder="templates", static_folder="static")

@crop_tracking_bp.route("/crop_tracking")
def crop_tracking():
    farms = UserCrop.query.filter_by(user_id=session["user_id"])
    return render_template("Crop_Tracking/crop_tracking.html", farms=farms, today=date.today())

@crop_tracking_bp.route("/api/crop_standards/<int:user_crop_id>")
def crop_standards(user_crop_id):
    # get_or_404() automatically returns a 404 error if ID not found
    growth_config = UserCrop.query.get_or_404(user_crop_id).standard.growth_config
    optimal_lcc = growth_config.get("optimal_lcc")
    stages = growth_config.get("stages")
    stages = list(stages.items())
    stages = sorted(stages, key=lambda x: x[1]["days_start"])
    return jsonify({"stages": stages, "optimal_lcc": optimal_lcc})

@crop_tracking_bp.route("/log_field_data/<int:user_crop_id>", methods=["POST"])
def log_field_data(user_crop_id):
    data = request.get_json()
    if not data:
        return jsonify({"alerts": ["No input data provided"]}), 400
    user_crop = UserCrop.query.get_or_404(user_crop_id)
    crop_log = CropLog.query.filter_by(user_crop_id=user_crop_id, log_date=date.today()).first()
    if not crop_log:
        crop_log = CropLog(
            user_crop_id=user_crop_id,
            log_date=date.today(),
            # (date.today() - user_crop.sowing_date) gives timedelta object
            week_number=int((date.today() - user_crop.sowing_date).days / 7) + 1,
            soil_moisture=data.get("moisture"),
            plant_height_cm=data.get("height"),
            lcc_score=data.get("lcc"),
            phenology_stage=data.get("stage"),
            stand_count=data.get("stand_count")
        )
        db.session.add(crop_log)
    else:
        crop_log.soil_moisture = data["moisture"] if data["moisture"] else crop_log.soil_moisture
        crop_log.plant_height_cm = data["height"] if data["height"] else crop_log.plant_height_cm
        crop_log.lcc_score = data["lcc"] if data["lcc"] else crop_log.lcc_score
        crop_log.phenology_stage = data["stage"] if data["stage"] else crop_log.phenology_stage
        crop_log.stand_count = data["stand_count"] if data["stand_count"] else crop_log.stand_count
    db.session.commit()
    return jsonify({"alerts": []})

@crop_tracking_bp.route("/add_farm", methods=["GET", "POST"])
def add_farm():
    if request.method == "POST":
        farm_name = request.form.get("farm_name")
        crop_id = request.form.get("crop_standard_id")
        sowing_date_str = request.form.get("sowing_date")
        area = request.form.get("area_acres")

        if not all([farm_name, crop_id, sowing_date_str]):
            return redirect(url_for('crop_tracking.add_farm'))

        try:
            new_farm = UserCrop(
                user_id=session.get('user_id'),
                crop_standard_id=int(crop_id),
                farm_name=farm_name,
                sowing_date=datetime.strptime(sowing_date_str, '%Y-%m-%d').date(),
                area_acres=float(area) if area else 1.0,
                status='active'
            )
            
            db.session.add(new_farm)
            db.session.commit()
            
            return redirect(url_for('crop_tracking.crop_tracking'))
            
        except Exception as e:
            db.session.rollback()
            return redirect(url_for('crop_tracking.add_farm'))

    all_crops = CropStandard.query.all()
    
    return render_template("Add_Farm/add_farm.html", crops=all_crops)

@crop_tracking_bp.route("/api/farm_analytics/<int:user_crop_id>")
def farm_analytics(user_crop_id):
    user_crop = UserCrop.query.get_or_404(user_crop_id)
    logs = user_crop.logs
    standard = user_crop.standard.growth_config

    # --- CHART 1: HEIGHT TREND (Expected vs Actual) ---
    plt.figure(figsize=(6, 4))
    
    # A. Plot Expected Growth (The "Reference Line")
    milestones = standard.get('height_milestones', {})
    if milestones:
        # Convert keys (weeks) to ints and sort them
        expected_weeks = sorted([int(k) for k in milestones.keys()])
        expected_heights = [milestones[str(w)] for w in expected_weeks]
        
        expected_weeks.insert(0, 0)
        expected_heights.insert(0, 0)
        
        plt.plot(expected_weeks, expected_heights, 
                 linestyle='--', color='green', alpha=0.5, label='Ideal Growth (TNAU)')

    # B. Plot Actual User Data
    if logs:
        # Filter logs that have height data
        height_logs = [l for l in logs if l.plant_height_cm is not None]
        if height_logs:
            actual_weeks = [l.week_number for l in height_logs]
            actual_heights = [l.plant_height_cm for l in height_logs]
            plt.plot(actual_weeks, actual_heights, 
                     marker='o', color='blue', linewidth=2, label='Your Farm')

    plt.title(f"Plant Height: {user_crop.farm_name}")
    plt.xlabel("Week Number")
    plt.ylabel("Height (cm)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Save Height Chart to Buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close() # CRITICAL: Free memory
    buf.seek(0)
    height_chart_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')


    # --- CHART 2: STAGE DURATION (Bar Chart) ---
    plt.figure(figsize=(6, 4))
    
    stages_config = standard.get('stages', {})
    # Sort stages by start day to ensure order (Veg -> Flow -> Mat)
    sorted_stages = sorted(stages_config.items(), key=lambda x: x[1]['days_start'])
    
    labels = [s[1]['label'] for s in sorted_stages]
    # Calculate duration: (End Day - Start Day)
    durations = [(s[1]['days_end'] - s[1]['days_start']) for s in sorted_stages]
    colors = ['#198754', '#ffc107', '#6c757d'] # Green, Yellow, Grey

    # Create Bar Chart
    bars = plt.bar(labels, durations, color=colors)
    
    plt.title("Expected Stage Duration (Days)")
    plt.ylabel("Days")
    plt.grid(axis='y', alpha=0.3)
    
    # Add text labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{int(height)} d',
                 ha='center', va='bottom')

    # Save Stage Chart to Buffer
    buf2 = io.BytesIO()
    plt.savefig(buf2, format='png', bbox_inches='tight')
    plt.close()
    buf2.seek(0)
    stage_chart_b64 = base64.b64encode(buf2.getvalue()).decode('utf-8')

    return jsonify({
        "height_chart": height_chart_b64, 
        "stage_chart": stage_chart_b64
    })