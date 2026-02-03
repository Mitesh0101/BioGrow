import joblib
import pandas as pd
import numpy as np

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