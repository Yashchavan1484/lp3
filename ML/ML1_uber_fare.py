"""ML1: Uber fare prediction - preprocessing, outliers, correlation,
Linear Regression vs Random Forest Regression.
Dataset: data/uber.csv  (https://www.kaggle.com/datasets/yasserh/uber-fares-dataset)
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # remove this line if you want plot windows
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split

# ---------- 1. Load & pre-process ----------
df = pd.read_csv("data/uber.csv")
print(df.head(), "\n")
df = df.drop(columns=[c for c in ("Unnamed: 0", "key") if c in df.columns])
print("Missing values:\n", df.isnull().sum(), "\n")
df = df.dropna()

df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"], errors="coerce")
df = df.dropna(subset=["pickup_datetime"])
df["hour"] = df["pickup_datetime"].dt.hour
df["day"] = df["pickup_datetime"].dt.day
df["month"] = df["pickup_datetime"].dt.month
df["year"] = df["pickup_datetime"].dt.year
df["dayofweek"] = df["pickup_datetime"].dt.dayofweek


def haversine(lat1, lon1, lat2, lon2):
    """Distance in km between pickup and drop-off."""
    lat1, lon1, lat2, lon2 = map(np.radians, (lat1, lon1, lat2, lon2))
    a = np.sin((lat2 - lat1) / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2
    return 6371 * 2 * np.arcsin(np.sqrt(a))


df["distance_km"] = haversine(df.pickup_latitude, df.pickup_longitude,
                              df.dropoff_latitude, df.dropoff_longitude)
df = df.drop(columns=["pickup_datetime"])

# ---------- 2. Outliers ----------
plt.figure(figsize=(10, 4))
df[["fare_amount", "distance_km"]].plot(kind="box", subplots=True, layout=(1, 2), figsize=(10, 4))
plt.savefig("ml1_boxplots_before.png")

# invalid coordinates / fares / passenger counts
df = df[(df.fare_amount > 0) & (df.distance_km > 0) & (df.distance_km < 100)]
df = df[df.pickup_latitude.between(-90, 90) & df.dropoff_latitude.between(-90, 90)]
df = df[df.pickup_longitude.between(-180, 180) & df.dropoff_longitude.between(-180, 180)]
df = df[df.passenger_count.between(1, 6)]
# IQR rule on fare
q1, q3 = df.fare_amount.quantile([0.25, 0.75])
iqr = q3 - q1
df = df[df.fare_amount.between(q1 - 1.5 * iqr, q3 + 1.5 * iqr)]
print("Rows after outlier removal:", len(df), "\n")

# ---------- 3. Correlation ----------
plt.figure(figsize=(9, 7))
sns.heatmap(df.corr(), annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Correlation matrix")
plt.tight_layout()
plt.savefig("ml1_correlation.png")
print("Correlation with fare_amount:\n", df.corr()["fare_amount"].sort_values(ascending=False), "\n")

# ---------- 4. Models ----------
X = df.drop(columns=["fare_amount"])
y = df["fare_amount"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

lr = LinearRegression().fit(X_train, y_train)
rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1).fit(X_train, y_train)

# ---------- 5. Evaluation ----------
results = []
for name, model in (("Linear Regression", lr), ("Random Forest", rf)):
    pred = model.predict(X_test)
    results.append({
        "Model": name,
        "R2": r2_score(y_test, pred),
        "RMSE": np.sqrt(mean_squared_error(y_test, pred)),
        "MAE": mean_absolute_error(y_test, pred),
    })
print(pd.DataFrame(results).to_string(index=False))
