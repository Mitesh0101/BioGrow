import joblib
import pandas as pd
import numpy as np

# Format: 'Crop Name': [Nitrogen (N), Phosphorus (P), Potassium (K)]
optimal_nutrient_dict = {
        'Cabbage': [124, 80, 100],
        'Pearl millet': [50, 30, 30],
        'annual moringa': [101, 50, 50],
        'ash gourd': [80, 60, 80],
        'beetroot': [79, 50, 50],
        'bengalgram': [50, 30, 30],
        'bhendi': [126, 80, 100],
        'bitter gourd': [80, 60, 80],
        'blackgram': [30, 30, 30],
        'bottle gourd': [80, 60, 80],
        'brinjal': [125, 60, 100],
        'capsicum': [124, 60, 100],
        'carrot': [100, 79, 80],
        'castor': [60, 30, 30],
        'cauliflower': [100, 50, 50],
        'chillies': [126, 59, 101],
        'chowchow': [80, 50, 50],
        'cluster bean': [80, 50, 50],
        'cotton': [100, 50, 50],
        'cowpea': [45, 30, 30],
        'cucumber': [80, 50, 50],
        'elephant foot yam': [80, 50, 50],
        'french bean': [79, 50, 50],
        'gingely': [30, 30, 30],
        'greengram': [30, 30, 30],
        'groundnut': [65, 50, 50],
        'horsegram': [50, 30, 30],
        'jute': [79, 40, 40],
        'kudiraivali': [50, 30, 30],
        'maize': [150, 75, 75],
        'muskmelon': [100, 50, 80],
        'onion': [125, 60, 100],
        'panivaragu': [35, 25, 25],
        'peas': [100, 50, 50],
        'pumpkin': [80, 60, 81],
        'radish': [80, 50, 50],
        'ragi': [35, 25, 25],
        'redgram': [50, 30, 30],
        'ribbed gourd': [80, 60, 80],
        'rice': [90, 50, 50],
        'samai': [35, 25, 25],
        'small onion': [80, 50, 50],
        'snake gourd': [80, 60, 80],
        'sorghum': [70, 50, 50],
        'soyabean': [65, 30, 30],
        'sugarbeet': [125, 70, 70],
        'sugarcane': [175, 80, 135],
        'sunflower': [60, 30, 30],
        'sweet potato': [100, 50, 50],
        'tapoica': [80, 50, 50],
        'thinai': [35, 25, 25],
        'tinda': [80, 50, 50],
        'tomato': [126, 60, 100],
        'varagu': [35, 25, 25],
        'vegetable cowpea': [79, 50, 50],
        'watermelon': [99, 50, 80],
        'wheat': [100, 50, 50],
}

# Helper: Convert dictionary keys to lowercase for easier matching
optimal_nutrient_dict_lower = {k.lower(): v for k, v in optimal_nutrient_dict.items()}

def load_model():
    # Load the model you saved
    model = joblib.load('crop_app.pkl')
    return model

def get_prediction(n, p, k, ph, temp, humidity, soil_type):
    model = load_model()

    # 1. Define the exact soil columns in the SAME ORDER as training X
    soil_columns = [
        'SOIL_Alluvial Soil', 'SOIL_Black Cotton Soil', 'SOIL_Black Soil',
        'SOIL_Brown Loamy Soil', 'SOIL_Clay Loamy Soil', 'SOIL_Clay Soil',
        'SOIL_Cotton Soil', 'SOIL_Deep Soil', 'SOIL_Friable Soil',
        'SOIL_Heavy Black Soil', 'SOIL_Heavy Soil', 'SOIL_Laterite Soil',
        'SOIL_Light Loamy Soil', 'SOIL_Light Soil', 'SOIL_Loamy Soil',
        'SOIL_Medium Black Soil', 'SOIL_Red Lateritic Loamy Soil',
        'SOIL_Red Loamy Soil', 'SOIL_Red Soil', 'SOIL_Rich Red Loamy Soil',
        'SOIL_Salty Clay Loamy Soil', 'SOIL_Sandy Clay Loamy Soil',
        'SOIL_Sandy Loamy Soil', 'SOIL_Sandy Soil',
        'SOIL_Shallow Black Soil', 'SOIL_Silty Loamy Soil',
        'SOIL_Well-Drained Loamy Soil', 'SOIL_Well-Drained Soil',
        'SOIL_Well-Grained Deep Loamy Moist Soil'
    ]

    # 2. Create the One-Hot Encoded Soil Vector (29 zeros, 1 one)
    soil_vector = [0] * len(soil_columns)
    
    # Construct the expected column name
    input_soil_col = f"SOIL_{soil_type}"
    
    if input_soil_col in soil_columns:
        index = soil_columns.index(input_soil_col)
        soil_vector[index] = 1
    else:
        print(f"Warning: Soil type '{soil_type}' not found in training data. Prediction may be inaccurate.")

    # 3. Combine basic features + soil vector
    # Order: N, P, K, SOIL_PH, TEMP, RELATIVE_HUMIDITY + 29 Soil Columns
    features = [n, p, k, ph, temp, humidity] + soil_vector

    # 4. Create DataFrame
    final_columns = ['N', 'P', 'K', 'SOIL_PH', 'TEMP', 'RELATIVE_HUMIDITY'] + soil_columns
    input_df = pd.DataFrame([features], columns=final_columns)

    # 5. Predict
    prediction = model.predict(input_df)
    return prediction[0]

def recommend_fertilizer(crop_name, current_n, current_p, current_k):
    # Normalize input
    crop_name = crop_name.strip().lower()
    
    if crop_name not in optimal_nutrient_dict_lower:
        return None

    target_n, target_p, target_k = optimal_nutrient_dict_lower[crop_name]
    
    recommendations = []
    
    # 1. Nitrogen Check
    if current_n < target_n:
        diff = target_n - current_n
        recommendations.append(f"Nitrogen (N) is LOW by {diff} kg/ha. Recommendation: Apply Urea or Ammonium Sulfate.")
    elif current_n > target_n:
        recommendations.append(f"Nitrogen (N) is HIGH. No N fertilizer needed.")
    else:
        recommendations.append("Nitrogen (N) levels are optimal.")

    # 2. Phosphorus Check
    if current_p < target_p:
        diff = target_p - current_p
        recommendations.append(f"Phosphorus (P) is LOW by {diff} kg/ha. Recommendation: Apply Superphosphate (SSP) or DAP.")
    elif current_p > target_p:
        recommendations.append(f"Phosphorus (P) is HIGH. No P fertilizer needed.")
    else:
        recommendations.append("Phosphorus (P) levels are optimal.")

    # 3. Potassium Check
    if current_k < target_k:
        diff = target_k - current_k
        recommendations.append(f"Potassium (K) is LOW by {diff} kg/ha. Recommendation: Apply Muriate of Potash (MOP).")
    elif current_k > target_k:
        recommendations.append(f"Potassium (K) is HIGH. No K fertilizer needed.")
    else:
        recommendations.append("Potassium (K) levels are optimal.")
        
    return recommendations