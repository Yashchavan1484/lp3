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


# This program predicts whether a bank customer will leave the bank (churn) using a neural network (ANN) built in Keras. I can’t see your output, so I haven’t invented any accuracy or confusion matrix numbers. Fill them in from your run.

# One thing to know before the viva: the comment in the code says “class weights”, but model.fit has no class_weight argument, so class weights are not applied. If asked, say “dropout and early stopping are used; class weights can be added with class_weight={0: 1, 1: 4}.”

# Aim
# To build a neural network that classifies whether a bank customer will leave (Exited = 1) or stay (Exited = 0), and evaluate it using accuracy and the confusion matrix.

# Theory
# This is a binary classification problem.
# Dataset: 10,000 customers, about 20% of whom churned, so the classes are imbalanced. A model that always says “stays” would already get about 80% accuracy.
# ANN: layers of neurons. Each neuron computes a weighted sum of its inputs plus a bias, then applies an activation function.
# ReLU = max(0, x). It is used in hidden layers and adds non-linearity.
# Sigmoid squeezes the output between 0 and 1, giving the probability of churn. If the probability is above 0.5, the prediction is “churn”.
# Binary cross-entropy is the loss for yes/no problems. It heavily punishes confident wrong predictions.
# Adam is an optimizer that adjusts weights by gradient descent with adaptive learning rates.
# Dropout (0.2): randomly switches off 20% of neurons during training, which reduces overfitting.
# Early stopping: stops training when validation loss stops improving for 10 epochs, and restores the best weights.
# One-hot encoding: converts categories (Geography, Gender) into 0/1 columns. drop="first" removes one column to avoid redundancy.
# Standardization: rescales each feature to mean 0 and standard deviation 1, which helps the network train faster and more stably.
# Fit on train only: the encoder and scaler learn from training data only, so no information leaks from the test set (data leakage).

# Steps (matches your code)
# Load the CSV.
# Drop RowNumber, CustomerId and Surname (identifiers with no predictive meaning) and Exited (the target) to get X, and take Exited as y.
# Stratified 80/20 train-test split.
# One-hot encode Geography and Gender. The other 8 numeric columns pass through unchanged.
# Standardize all features (11 in total).
# Build the network: 11 inputs, then Dense(16), Dropout(0.2), Dense(8) and Dense(1, sigmoid).
# Compile with Adam and binary cross-entropy, and train for up to 100 epochs with batch size 32, using 20% of the training data for validation and early stopping.
# Predict probabilities on the test set, threshold at 0.5, and print accuracy and the confusion matrix.

# Tables to paste into GitHub

# 1. Pipeline summary

# markdown
# | Step | Operation                                   | Purpose                                      |
# |------|---------------------------------------------|----------------------------------------------|
# | 1    | Load CSV                                    | Read 10,000 customer records                 |
# | 2    | Drop RowNumber, CustomerId, Surname, Exited | Remove IDs and separate the target           |
# | 3    | Stratified 80/20 split                      | Same churn ratio in train and test           |
# | 4    | One-hot encode Geography and Gender         | Convert text categories to numbers           |
# | 5    | StandardScaler                              | Put all features on the same scale           |
# | 6    | Build ANN (16, 8, 1)                        | Learn non-linear churn patterns              |
# | 7    | Train with Adam, dropout, early stopping    | Reduce overfitting and stop at the best point |
# | 8    | Accuracy and confusion matrix               | Evaluate on unseen customers                 |

# 2. Network architecture (11 input features after encoding)

# markdown
# | Layer     | Neurons | Activation | Parameters (weights + biases) | Calculation      |
# |-----------|---------|------------|-------------------------------|------------------|
# | Input     | 11      | -          | 0                             | -                |
# | Dense 1   | 16      | ReLU       | 192                           | 11 × 16 + 16     |
# | Dropout   | -       | -          | 0                             | Drops 20% in training only |
# | Dense 2   | 8       | ReLU       | 136                           | 16 × 8 + 8       |
# | Output    | 1       | Sigmoid    | 9                             | 8 × 1 + 1        |
# | **Total** |         |            | **337**                       |                  |

# 3. Key settings

# markdown
# | Setting             | Value                | Why                                              |
# |---------------------|----------------------|--------------------------------------------------|
# | Hidden activation   | ReLU                 | Fast, avoids vanishing gradients                 |
# | Output activation   | Sigmoid              | Gives churn probability between 0 and 1          |
# | Loss                | Binary cross-entropy | Standard loss for 2-class problems               |
# | Optimizer           | Adam                 | Adaptive learning rate, converges quickly        |
# | Batch size          | 32                   | Weights updated after every 32 samples           |
# | Max epochs          | 100                  | Early stopping usually ends training sooner      |
# | Dropout             | 0.2                  | Reduces overfitting                              |
# | Early stopping      | patience = 10        | Stops when validation loss stops improving       |
# | Decision threshold  | 0.5                  | Above 0.5 means predicted churn                  |

# 4. Confusion matrix meaning

# markdown
# |                  | Predicted Stays                        | Predicted Churns                          |
# |------------------|----------------------------------------|-------------------------------------------|
# | Actual Stays     | TN (correctly predicted loyal)         | FP (false alarm, wasted retention offer)  |
# | Actual Churns    | FN (churner missed, customer lost)     | TP (churner caught correctly)             |

# 5. Results (fill from your output)

# markdown
# | Metric           | Value |
# |------------------|-------|
# | Test accuracy    |       |
# | TN               |       |
# | FP               |       |
# | FN               |       |
# | TP               |       |

# 6. Complexity (n = training samples, d = 11 features, P = 337 parameters, E = epochs run)

# markdown
# | Part                 | Time Complexity       | Space Complexity | Reason                                             |
# |----------------------|-----------------------|------------------|----------------------------------------------------|
# | Preprocessing        | O(n·d)                | O(n·d)           | One pass over the data                             |
# | Training             | O(E · n · P)          | O(P + batch)     | Each epoch does a forward and backward pass per sample |
# | Prediction (1 row)   | O(P)                  | O(P)             | One forward pass through 337 weights               |
# | Model storage        | -                     | O(P)             | Only 337 numbers are stored                        |

# For deeper networks, P = sum over layers of (inputs × neurons).

# 7. Model comparison (no numbers are claimed. Check your own results)

# markdown
# | Point                    | Neural Network (this code)          | Logistic Regression              | Random Forest                     |
# |--------------------------|-------------------------------------|----------------------------------|-----------------------------------|
# | Decision boundary        | Non-linear, flexible                | Linear only                      | Non-linear, piecewise             |
# | Feature scaling needed   | Yes                                 | Yes (helpful)                    | No                                |
# | Training time            | Slowest (many epochs)               | Very fast                        | Moderate                          |
# | Prediction time          | Fast                                | Very fast                        | Slower (many trees)               |
# | Interpretability         | Low (black box)                     | High (coefficients)              | Medium (feature importance)       |
# | Data needed              | Benefits from more data             | Works with little data           | Works well with moderate data     |
# | Overfitting control      | Dropout, early stopping             | Regularization                   | Averaging many trees              |
# | Tabular data like this   | Good, but not always the best       | Good baseline                    | Often equal or better             |
# | Memory                   | Small here (337 parameters)         | Tiny                             | Large                             |
# Why use a neural network here (and an honest note)
# Churn depends on combinations of features (older customers with a high balance and a single product churn more). A neural network learns such interactions automatically, while logistic regression cannot.
# Standardization, dropout and early stopping make training stable and prevent memorizing the training data.
# Honest point for the viva: on small tabular data like this (10,000 rows), tree models such as Random Forest or XGBoost often perform as well as or better than neural networks. The ANN is chosen to demonstrate deep learning, and it is a good fit when more data or more complex patterns are available.
# Accuracy alone is misleading because only about 20% of customers churn. Check the confusion matrix, and ideally recall, precision and F1.
# Easy example

# Think of a bank manager deciding who will leave. Logistic regression is like a fixed checklist: “age adds 2 points, balance adds 1 point”. The neural network is like a small team of staff: the first layer notices simple signals (“older”, “inactive”, “has only one product”), the next layer combines them (“older and inactive”), and the final neuron gives a probability such as 0.73. Above 0.5 means “likely to leave, offer a retention deal”.

# Mini forward pass for one neuron:

# markdown
# | Input        | Value | Weight | Product |
# |--------------|-------|--------|---------|
# | Age (scaled) | 1.2   | 0.8    | 0.96    |
# | Active (scaled) | -1.0 | 0.5  | -0.50   |
# | Bias         | -     | -      | 0.10    |
# | **Sum**      |       |        | **0.56** |

# ReLU(0.56) = 0.56 is passed to the next layer. At the end, sigmoid turns the final sum into a probability.
