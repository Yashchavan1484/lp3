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


# Aim
# To predict whether a patient has diabetes using KNN, and evaluate the model using the confusion matrix, accuracy, error rate, precision and recall.

# Theory
# This is a binary classification problem: Outcome = 1 means diabetic, 0 means not diabetic.
# Dataset: the Pima diabetes data, usually 768 patients with 8 features (Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age). About 35% are diabetic, so the classes are slightly imbalanced.
# KNN finds the k nearest training patients (k = 5) using Euclidean distance and takes a majority vote. It is a lazy learner, because it only stores the data and does the work at prediction time.
# Missing values hidden as zeros: a glucose, blood pressure, skin thickness, insulin or BMI of 0 is impossible. These zeros are converted to NaN and replaced by the median, which is not affected by outliers. Pregnancies = 0 is valid, so it is left alone.
# Scaling is essential for KNN: Insulin (up to about 800) would dominate Age (about 20 to 80) in the distance calculation. StandardScaler gives every feature mean 0 and standard deviation 1.
# Stratified split: the same diabetic ratio in train and test.

# Steps (matches your code)
# Load the CSV.
# Replace impossible zeros in 5 columns with NaN, then fill them with the column median.
# Separate X (features) and y (Outcome).
# Stratified 80/20 split.
# Standardize (fit on train, transform on test).
# Train KNN with k = 5 and predict on the test set.
# Print the confusion matrix, TN, FP, FN, TP, accuracy, error rate, precision and recall.

# Tables to paste into GitHub

# 1. Pipeline summary

# markdown
# | Step | Operation                                   | Purpose                                         |
# |------|---------------------------------------------|-------------------------------------------------|
# | 1    | Load CSV                                    | Read patient records                            |
# | 2    | Replace 0 with NaN in 5 columns             | Zero is impossible for these measurements       |
# | 3    | Fill NaN with median                        | Robust replacement, not affected by outliers    |
# | 4    | Separate X and y (Outcome)                  | Features and target                             |
# | 5    | Stratified 80/20 split                      | Same diabetic ratio in train and test           |
# | 6    | StandardScaler                              | KNN is distance based, so scales must be equal  |
# | 7    | Train KNN (k = 5)                           | Store the training data                         |
# | 8    | Confusion matrix and metrics                | Evaluate on unseen patients                     |

# 2. Confusion matrix meaning

# markdown
# |                    | Predicted Not Diabetic                   | Predicted Diabetic                         |
# |--------------------|------------------------------------------|--------------------------------------------|
# | Actual Not Diabetic| TN (healthy, correctly identified)       | FP (healthy, wrongly flagged)              |
# | Actual Diabetic    | FN (diabetic missed, dangerous)          | TP (diabetic correctly detected)           |

# 3. Metric formulas

# markdown
# | Metric     | Formula                    | Meaning                                              |
# |------------|----------------------------|------------------------------------------------------|
# | Accuracy   | (TP + TN) / Total          | Fraction of all predictions that are correct         |
# | Error rate | (FP + FN) / Total = 1 - Acc| Fraction of predictions that are wrong               |
# | Precision  | TP / (TP + FP)             | Of patients predicted diabetic, how many truly are   |
# | Recall     | TP / (TP + FN)             | Of all truly diabetic patients, how many were found  |

# 4. Worked example (illustration only, not your result)

# Suppose the test set has 154 patients and the confusion matrix gives TN = 80, FP = 20, FN = 25, TP = 29.

# markdown
# | Metric     | Calculation        | Value  |
# |------------|--------------------|--------|
# | Accuracy   | (29 + 80) / 154    | 0.7078 |
# | Error rate | (20 + 25) / 154    | 0.2922 |
# | Precision  | 29 / (29 + 20)     | 0.5918 |
# | Recall     | 29 / (29 + 25)     | 0.5370 |

# 5. Your results (fill from your output)

# markdown
# | Metric     | Value |
# |------------|-------|
# | TN         |       |
# | FP         |       |
# | FN         |       |
# | TP         |       |
# | Accuracy   |       |
# | Error rate |       |
# | Precision  |       |
# | Recall     |       |

# 6. Complexity (n = training patients, d = 8 features, m = test patients)

# markdown
# | Part                 | Time Complexity               | Space Complexity | Reason                                                          |
# |----------------------|-------------------------------|------------------|-----------------------------------------------------------------|
# | Preprocessing        | O(n·d) (median needs O(n log n) sorting per column) | O(n·d) | Pass over the data                          |
# | KNN training         | O(1), or O(n log n) with a KD-tree | O(n·d)      | Only stores the data (sklearn may build a tree index)           |
# | KNN prediction       | O(n·d) per patient (brute force) | O(n·d)        | Distance to every training patient, then pick the 5 smallest    |
# | Total prediction     | O(m·n·d)                      | O(n·d)           | Repeated for all m test patients                                |

# 7. Model comparison (no numbers claimed, check your own results)

# markdown
# | Point                   | KNN (this code)                     | Logistic Regression              | Random Forest                    |
# |-------------------------|-------------------------------------|----------------------------------|----------------------------------|
# | Type                    | Instance-based, lazy learner        | Linear model                     | Ensemble of trees                |
# | Training time           | None                                | Very fast                        | Moderate                         |
# | Prediction time         | Slow for large data                 | Very fast                        | Moderate                         |
# | Feature scaling         | Required                            | Helpful                          | Not needed                       |
# | Assumptions about data  | None (non-parametric)               | Linear relationship              | None                             |
# | Handles non-linear data | Yes                                 | No                               | Yes                              |
# | Interpretability        | Easy idea, no model to inspect      | High (coefficients)              | Medium (feature importance)      |
# | Sensitive to noise      | Yes, especially for small k         | Less                             | Less                             |
# | Memory                  | Stores all training data            | Tiny                             | Large                            |
# | Best for                | Small datasets, simple baseline     | Quick, explainable baseline      | Higher accuracy on tabular data  |
# Why KNN (and an honest note)
# It is simple and needs no training or assumptions about the data’s shape, so it is a good baseline for a small dataset like this (768 rows). Prediction is fast enough because n is small.
# Median imputation and scaling matter more than anything else here. Without scaling, Insulin and Glucose would dominate the distance and KNN would perform poorly.
# Honest point for the viva: on this dataset, Logistic Regression or Random Forest often match or beat KNN. KNN slows down on big data and suffers when there are many irrelevant features.
# In a medical problem recall matters more than precision. A missed diabetic patient (FN) is worse than a false alarm (FP), because the false alarm can be cleared with a further test.
# Easy example

# You are new to a town and want to know if a house is expensive. You ask the 5 nearest neighbors and go with the majority. KNN does the same: to classify a new patient, it finds the 5 most similar patients (by glucose, BMI, age, etc.) and copies the majority outcome.

# Mini KNN example (k = 3, two scaled features):

# markdown
# | Training patient | Glucose (scaled) | BMI (scaled) | Outcome      | Distance to new patient (1.3, 0.9) |
# |------------------|------------------|--------------|--------------|-------------------------------------|
# | P1               | 1.5              | 1.0          | Diabetic     | 0.22                                |
# | P2               | 1.2              | 0.8          | Diabetic     | 0.14                                |
# | P3               | -0.5             | -0.3         | Not Diabetic | 2.16                                |
# | P4               | -0.8             | -0.6         | Not Diabetic | 2.58                                |
# | P5               | 1.0              | 1.2          | Diabetic     | 0.42                                |
# | P6               | 0.0              | 0.0          | Not Diabetic | 1.58                                |

# The 3 nearest are P2, P1 and P5, all Diabetic, so the new patient is predicted Diabetic.

# Distance formula: d = √[(x₁ − x₂)² + (y₁ − y₂)²]. For P2: √(0.1² + 0.1²) ≈ 0.14.


