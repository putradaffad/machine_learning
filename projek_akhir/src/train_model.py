import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
from utils import load_dataset

def train_and_save_model():
    df = load_dataset()
    X = df[['terlambat_1', 'terlambat_2', 'terlambat_3']]
    y = df['target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("Akurasi:", accuracy_score(y_test, y_pred))

    joblib.dump(model, 'model/model.pkl')
