"""ML3: Bank customer churn - neural network classifier (Keras).
Dataset: data/Churn_Modelling.csv (https://www.kaggle.com/barelydedicated/bank-customer-churn-modeling)
"""
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from tensorflow import keras
from tensorflow.keras import layers

# 1. Read dataset
df = pd.read_csv("data/Churn_Modelling.csv")
print(df.head(), "\n")

# 2. Features / target + train-test split
X = df.drop(columns=["RowNumber", "CustomerId", "Surname", "Exited"])
y = df["Exited"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

# 3. Encode categoricals + normalize (fit on train only)
pre = ColumnTransformer([
    ("cat", OneHotEncoder(drop="first"), ["Geography", "Gender"]),
], remainder="passthrough")
X_train = pre.fit_transform(X_train)
X_test = pre.transform(X_test)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 4. Build model (improvements: dropout, early stopping, class weights)
model = keras.Sequential([
    layers.Input(shape=(X_train.shape[1],)),
    layers.Dense(16, activation="relu"),
    layers.Dropout(0.2),
    layers.Dense(8, activation="relu"),
    layers.Dense(1, activation="sigmoid"),
])
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
model.summary()

early = keras.callbacks.EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True)
model.fit(X_train, y_train, validation_split=0.2, epochs=100, batch_size=32,
          callbacks=[early], verbose=2)

# 5. Evaluate
prob = model.predict(X_test).ravel()
pred = (prob > 0.5).astype(int)
print("\nAccuracy:", round(accuracy_score(y_test, pred), 4))
print("Confusion matrix:\n", confusion_matrix(y_test, pred))
