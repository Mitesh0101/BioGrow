from flask import Blueprint, render_template, request, jsonify
from utils.prediction_model import get_prediction

crop_prediction_bp = Blueprint("crop_prediction", __name__)

@crop_prediction_bp.route("/crop_prediction")
def crop_prediction():
        return render_template("Crop_Prediction/crop_prediction.html")

@crop_prediction_bp.route("/api/predict-crop", methods=["POST"])
def predict_crop():
    data = request.get_json()

    result = get_prediction(data['n'], data['p'], data['k'], data['ph'], data['temp'],
                            data['humidity'], data['soil_type'])
    
    return jsonify({'result': result})