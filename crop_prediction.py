from flask import Blueprint, render_template, request, jsonify, make_response, json, session
from utils.prediction_model import get_prediction, recommend_fertilizer
from models import CropStandard, PredictionReport
from utils.water_requirements import crop_water_requirements
import pdfkit
import os
import dotenv
from extensions import db

dotenv.load_dotenv()
crop_prediction_bp = Blueprint("crop_prediction", __name__)

@crop_prediction_bp.route("/crop_prediction")
def crop_prediction():
        return render_template("Crop_Prediction/crop_prediction.html")

@crop_prediction_bp.route("/api/predict-crop", methods=["POST"])
def predict_crop():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    try:
        result, match_percentage = get_prediction(float(data["n"]),
                                                  float(data["p"]),
                                                  float(data["k"]),
                                                  float(data["ph"]),
                                                  float(data["temp"]),
                                                  float(data["humidity"]),
                                                  data["soil_type"])
        
        recommendations = recommend_fertilizer(result,
                                               float(data["n"]),
                                               float(data["p"]),
                                               float(data["k"]))

        standard = CropStandard.query.filter_by(crop_name=result).first()

        new_report = PredictionReport(
            user_id=session.get("user_id"),
            n=data['n'], p=data['p'], k=data['k'],
            ph=data['ph'], humidity=data['humidity'],
            temperature=data['temp'], soil_type=data['soil_type'],
            crop_name=result,
            match_percentage=float(match_percentage),
            water_req=crop_water_requirements.get(result),
            harvest_duration = f"{standard.growth_config.get("total_duration_days")[0]} - {standard.growth_config.get("total_duration_days")[1]}",
            recommendations_json=json.dumps(recommendations) # Convert Python list to JSON string
        )
        
        db.session.add(new_report)
        db.session.commit()

        return jsonify({"result": result,
                        "match_percentage": match_percentage,
                        "recommendations": recommendations,
                        "duration": standard.growth_config.get("total_duration_days"),
                        "water_req": crop_water_requirements.get(result),
                        "report_id": new_report.report_id})
    
    except KeyError as e:
        # Tells the frontend EXACTLY which field is missing (e.g., 'n')
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    
    except ValueError as e:
        # Tells the frontend they sent text instead of a number
        return jsonify({"error": "Invalid number format. Please ensure N, P, K, pH, Temp, and Humidity are numbers."}), 400
    
    except Exception as e:
        # Catch-all for anything else (like the model crashing)
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

@crop_prediction_bp.route('/download_report/<report_id>', methods=['GET'])
def download_report(report_id):
    # Fetch the exact report from the DB
    report = PredictionReport.query.get_or_404(report_id)

    if not session.get("user_id"):
        return jsonify({"error": "Please Login First"}), 403

    if report.user_id != session.get("user_id"):
        return jsonify({"error": "Unauthorized Access Banned!"}), 403
    
    # Reconstruct the data dictionary for your PDF HTML template
    data_for_pdf = {
        "report_date": report.created_at.strftime("%Y-%m-%d %H:%M"),
        "report_id": report.report_id,
        "current_year": report.created_at.year,
        "inputs": {
             "n": report.n, "p": report.p, "k": report.k, 
             "ph": report.ph, "temp": report.temperature, 
             "humidity": report.humidity, "soil_type": report.soil_type
        },
        "result": {
            "crop_name": report.crop_name,
            "match_percentage": report.match_percentage,
            "water_requirement": report.water_req,
            "harvest_duration": report.harvest_duration,
            "recommendations": json.loads(report.recommendations_json) # Parse back to list
        }
    }

    # Render template and generate PDF via pdfkit just like before...
    rendered_html = render_template('pdf_report.html', **data_for_pdf)
    config = pdfkit.configuration(wkhtmltopdf=os.getenv("PATH_WKHTMLTOPDF"))
    # The output_path is set to False so the pdf is not saved on the server
    pdf = pdfkit.from_string(rendered_html, False, configuration=config)
    
    response = make_response(pdf)
    # Force the browser to recognize the incoming binary stream as a PDF document.
    response.headers['Content-Type'] = 'application/pdf'
    # 'attachment' explicitly triggers the OS download dialog instead of opening the file in a new tab.
    response.headers['Content-Disposition'] = f'attachment; filename=BioGrow_{report.crop_name.capitalize()}.pdf'
    return response