"""OPTIONAL: creates small synthetic stand-ins for the Kaggle CSVs so you can
test the scripts offline. Use the real Kaggle datasets for your submission."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(0)

# Uber
n = 3000
d = pd.DataFrame({
    "Unnamed: 0": range(n), "key": range(n),
    "pickup_datetime": pd.to_datetime("2012-01-01") + pd.to_timedelta(rng.integers(0, 3e7, n), unit="m"),
    "pickup_longitude": -73.98 + rng.normal(0, .02, n), "pickup_latitude": 40.75 + rng.normal(0, .02, n),
    "dropoff_longitude": -73.97 + rng.normal(0, .02, n), "dropoff_latitude": 40.76 + rng.normal(0, .02, n),
    "passenger_count": rng.integers(1, 6, n)})
dist = np.hypot(d.pickup_longitude - d.dropoff_longitude, d.pickup_latitude - d.dropoff_latitude) * 111
d["fare_amount"] = 2.5 + 2.2 * dist + rng.normal(0, 1, n)
d.loc[:5, "fare_amount"] = -3  # a few bad rows
d.to_csv("data/uber.csv", index=False)

# Email spam
words = [f"w{i}" for i in range(100)]
y = rng.integers(0, 2, 600)
m = rng.poisson(1, (600, 100)) + (y[:, None] * rng.poisson(1.5, (600, 100)) * (np.arange(100) < 20))
e = pd.DataFrame(m, columns=words)
e.insert(0, "Email No.", [f"Email {i}" for i in range(600)])
e["Prediction"] = y
e.to_csv("data/emails.csv", index=False)

# Churn
n = 2000
c = pd.DataFrame({
    "RowNumber": range(n), "CustomerId": range(n), "Surname": "X",
    "CreditScore": rng.integers(350, 850, n), "Geography": rng.choice(["France", "Spain", "Germany"], n),
    "Gender": rng.choice(["Male", "Female"], n), "Age": rng.integers(18, 80, n),
    "Tenure": rng.integers(0, 10, n), "Balance": rng.uniform(0, 2e5, n),
    "NumOfProducts": rng.integers(1, 4, n), "HasCrCard": rng.integers(0, 2, n),
    "IsActiveMember": rng.integers(0, 2, n), "EstimatedSalary": rng.uniform(1e4, 2e5, n)})
c["Exited"] = ((c.Age > 50).astype(int) + rng.random(n) > 1.0).astype(int)
c.to_csv("data/Churn_Modelling.csv", index=False)

# Diabetes
n = 700
g = pd.DataFrame({
    "Pregnancies": rng.integers(0, 10, n), "Glucose": rng.integers(0, 200, n),
    "BloodPressure": rng.integers(0, 120, n), "SkinThickness": rng.integers(0, 50, n),
    "Insulin": rng.integers(0, 300, n), "BMI": rng.uniform(0, 50, n),
    "DiabetesPedigreeFunction": rng.uniform(0, 2, n), "Age": rng.integers(21, 80, n)})
g["Outcome"] = (g.Glucose + rng.normal(0, 40, n) > 120).astype(int)
g.to_csv("data/diabetes.csv", index=False)

# Sales
n = 1000
s = pd.DataFrame({"QUANTITYORDERED": rng.integers(10, 60, n), "PRICEEACH": rng.uniform(30, 100, n),
                  "MSRP": rng.integers(40, 200, n)})
s["SALES"] = s.QUANTITYORDERED * s.PRICEEACH
s.to_csv("data/sales_data_sample.csv", index=False)
print("Sample data written to data/")
