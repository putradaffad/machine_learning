import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

def train_and_save_model():
    df = pd.read_csv('data/dataset.csv')
    X = df[['terlambat_1', 'terlambat_2', 'terlambat_3', 'terlambat_4', 'terlambat_5']]
    y = df['target']
    model = RandomForestClassifier()
    model.fit(X, y)
    joblib.dump(model, 'model/model.pkl')
