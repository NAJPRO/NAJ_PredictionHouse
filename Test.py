import pandas as pd
import joblib

data = joblib.load("zillow_random_forest_model_joblib_version1.2.pkl")
print(type(data))