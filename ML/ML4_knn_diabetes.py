"""ML4: KNN on diabetes.csv - confusion matrix, accuracy, error rate, precision, recall.
Dataset: data/diabetes.csv (https://www.kaggle.com/datasets/abdallamahgoub/diabetes)
"""
import numpy as np
import pandas as pd
from sklearn.metrics import (accuracy_score, confusion_matrix,
                             precision_score, recall_score)
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("data/diabetes.csv")
print(df.head(), "\n")

# columns where 0 is physiologically impossible -> treat as missing, fill with median
for col in ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]:
    if col in df.columns:
        df[col] = df[col].replace(0, np.nan)
        df[col] = df[col].fillna(df[col].median())

X = df.drop(columns=["Outcome"])
y = df["Outcome"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)
pred = knn.predict(X_test)

cm = confusion_matrix(y_test, pred)
tn, fp, fn, tp = cm.ravel()
acc = accuracy_score(y_test, pred)
print("Confusion matrix:\n", cm)
print(f"TN={tn}  FP={fp}  FN={fn}  TP={tp}")
print(f"Accuracy   : {acc:.4f}")
print(f"Error rate : {1 - acc:.4f}")
print(f"Precision  : {precision_score(y_test, pred):.4f}")
print(f"Recall     : {recall_score(y_test, pred):.4f}")
