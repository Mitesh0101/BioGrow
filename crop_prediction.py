from flask import Blueprint, render_template, request, jsonify
from utils.prediction_model import get_prediction, recommend_fertilizer

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
        result = get_prediction(float(data["n"]), float(data["p"]), float(data["k"]), float(data["ph"]), float(data["temp"]),
                                float(data["humidity"]), data["soil_type"])
        
        recommendations = recommend_fertilizer(result, float(data["n"]), float(data["p"]), float(data["k"]))

        return jsonify({"result": result, "recommendations": recommendations})
    
    except KeyError as e:
        # Tells the frontend EXACTLY which field is missing (e.g., 'n')
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    
    except ValueError as e:
        # Tells the frontend they sent text instead of a number
        return jsonify({"error": "Invalid number format. Please ensure N, P, K, pH, Temp, and Humidity are numbers."}), 400
    
    except Exception as e:
        # Catch-all for anything else (like the model crashing)
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500