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
