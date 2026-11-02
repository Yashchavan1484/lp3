"""ML2: Email spam detection using K-Nearest Neighbors and SVM.
Dataset: data/emails.csv (https://www.kaggle.com/datasets/balaka18/email-spam-classification-dataset-csv)
"""
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

df = pd.read_csv("data/emails.csv")
print("Shape:", df.shape)
print("Missing values:", df.isnull().sum().sum())
print("Class counts (0 = not spam, 1 = spam):\n", df["Prediction"].value_counts(), "\n")

X = df.drop(columns=["Email No.", "Prediction"])
y = df["Prediction"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

models = {
    "K-Nearest Neighbors (k=5)": KNeighborsClassifier(n_neighbors=5),
    "Support Vector Machine (linear)": SVC(kernel="linear", C=1.0),
}
scores = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    scores[name] = accuracy_score(y_test, pred)
    print("=" * 60)
    print(name)
    print("Accuracy:", round(scores[name], 4))
    print("Confusion matrix:\n", confusion_matrix(y_test, pred))
    print(classification_report(y_test, pred, target_names=["Not Spam", "Spam"]))

best = max(scores, key=scores.get)
print("Best performing model:", best)


# Aim
# To classify emails as spam or not spam using KNN and a linear SVM, and compare them using accuracy, the confusion matrix and the classification report.

# Theory
# This is a classification problem (the output is a category, not a number).
# Dataset: each row is an email, and each of the roughly 3000 columns is the count of a common word (such as “free” or “offer”). Prediction is 1 for spam and 0 for not spam. So there are about 3000 features.
# KNN: finds the k closest training emails (k = 5) and takes a majority vote of their labels. It does no real training and just stores the data (a “lazy learner”).
# SVM: finds the best separating line (hyperplane) between spam and not-spam with the maximum margin. Only the points nearest the boundary (support vectors) matter. kernel="linear" means a straight boundary. C=1.0 controls how strictly mistakes are punished.
# Stratified split: keeps the same spam to non-spam ratio in both train and test sets, which is important because the classes are imbalanced.

# Steps (matches your code)
# Load the CSV and print the shape, missing values and class counts.
# Drop Email No. (just an ID) and Prediction (the label) to get X, and take Prediction as y.
# Split 80/20 with stratify=y and random_state=42.
# Train KNN (k = 5) and SVM (linear).
# Predict on the test set and compute accuracy, the confusion matrix and the classification report.
# Pick the model with the highest accuracy.


# 1. Pipeline summary

# markdown
# | Step | Operation                                | Purpose                                   |
# |------|------------------------------------------|-------------------------------------------|
# | 1    | Load CSV, check shape and missing values | Understand the data                       |
# | 2    | Check class counts                       | Detect class imbalance                    |
# | 3    | Drop `Email No.` and `Prediction`        | Keep only word-count features in X        |
# | 4    | Stratified 80/20 split                   | Same spam ratio in train and test         |
# | 5    | Train KNN (k=5) and linear SVM           | Two different classifiers to compare      |
# | 6    | Accuracy, confusion matrix, report       | Evaluate on unseen emails                 |
# | 7    | Choose the highest accuracy              | Select the best model                     |

# 2. Confusion matrix meaning

# markdown
# |                  | Predicted Not Spam                | Predicted Spam                    |
# |------------------|-----------------------------------|-----------------------------------|
# | Actual Not Spam  | TN (correctly kept in inbox)      | FP (good email sent to spam, bad) |
# | Actual Spam      | FN (spam reached inbox)           | TP (spam correctly caught)        |

# 3. Evaluation metrics

# markdown
# | Metric    | Formula                     | Meaning                                         |
# |-----------|-----------------------------|-------------------------------------------------|
# | Accuracy  | (TP + TN) / Total           | Overall fraction of correct predictions         |
# | Precision | TP / (TP + FP)              | Of the emails marked spam, how many truly were  |
# | Recall    | TP / (TP + FN)              | Of all real spam, how much was caught           |
# | F1-score  | 2 × P × R / (P + R)         | Balance of precision and recall                 |

# 4. Results (fill from your output)

# markdown
# | Model                           | Accuracy | Precision (Spam) | Recall (Spam) | F1 (Spam) |
# |---------------------------------|----------|------------------|---------------|-----------|
# | K-Nearest Neighbors (k=5)       |          |                  |               |           |
# | Support Vector Machine (linear) |          |                  |               |           |

# 5. Complexity (n = training emails, d = features ≈ 3000, m = test emails, SV = support vectors)

# markdown
# | Part                | Time Complexity            | Space Complexity | Reason                                                   |
# |---------------------|----------------------------|------------------|----------------------------------------------------------|
# | KNN training        | O(1)                       | O(n·d)           | Only stores the data                                     |
# | KNN prediction      | O(n·d) per email           | O(n·d)           | Distance to every training email, then pick 5 smallest   |
# | SVM training        | Between O(n²·d) and O(n³)  | O(n²) kernel cache | Solves a quadratic optimization problem               |
# | SVM prediction      | O(SV·d) per email          | O(SV·d)          | Compares with the support vectors only                   |

# 6. Model comparison

# markdown
# | Point                      | K-Nearest Neighbors                          | SVM (linear)                                      |
# |----------------------------|----------------------------------------------|---------------------------------------------------|
# | Type                       | Instance-based (lazy learner)                | Margin-based, learns a boundary                   |
# | Training time              | None                                         | Slow for very large n                             |
# | Prediction time            | Slow (checks all training emails)            | Fast (uses only support vectors)                  |
# | High-dimensional data      | Weak (curse of dimensionality)               | Strong, designed for many features                |
# | Sparse text data           | Distances become less meaningful             | Works very well                                   |
# | Feature scaling            | Sensitive (needed)                           | Sensitive (helpful)                               |
# | Noise / outliers           | Sensitive to noisy neighbors                 | Robust because of the margin and C                |
# | Needs to store dataset     | Yes, all of it                               | No, only support vectors                          |
# | Hyperparameters            | k, distance metric                           | C, kernel                                         |
# | Accuracy on spam data      | Lower (expected)                             | Higher (expected)                                 |
# Why SVM is better here
# With about 3000 features, every email is a point in a 3000-dimensional space. There, distances between points become similar to each other, so KNN’s “nearest neighbors” are not very meaningful.
# Spam and non-spam emails are often close to linearly separable in word-count space, which is exactly what a linear SVM handles best.
# The maximum-margin idea gives a boundary that generalizes well to unseen emails.
# At prediction time SVM only uses support vectors, while KNN compares against all training emails.
# Trade-off: KNN is simple, needs no training and is easy to explain. SVM takes longer to train on huge datasets.

# If your output shows something different, explain it honestly in the viva (for example, k or the lack of scaling affected KNN).

# Easy example
# KNN is like asking your 5 nearest neighbors whether an email looks like spam. The majority wins. If your neighbors are confused (noisy, high-dimensional data), the answer is poor.
# SVM is like drawing the widest possible road between spam emails and normal emails. A new email is classified by which side of the road it falls on.

# Mini KNN example (2 words only: “free”, “meeting”):

# markdown
# | Training email | "free" count | "meeting" count | Label    | Distance to new email (4, 0) |
# |----------------|--------------|-----------------|----------|------------------------------|
# | E1             | 5            | 0               | Spam     | 1.0                          |
# | E2             | 3            | 1               | Spam     | 1.4                          |
# | E3             | 0            | 4               | Not Spam | 5.7                          |
# | E4             | 1            | 3               | Not Spam | 4.2                          |
# | E5             | 4            | 1               | Spam     | 1.0                          |

# With k = 3, the nearest are E1, E5 and E2, all Spam, so the new email is classified as Spam.
