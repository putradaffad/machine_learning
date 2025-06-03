import joblib
import numpy as np

def predict_late(input_data):
    model = joblib.load('model/model.pkl')
    input_array = np.array(input_data).reshape(1, -1)
    prediction = model.predict(input_array)
    return prediction[0]
