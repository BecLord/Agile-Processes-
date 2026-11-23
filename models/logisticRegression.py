# Scam Shield - Agile Processes
# Logistic Regression Model
# Classify human and AI-generated voice recordings

from pathlib import Path

import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# Step 1: Locate project files

project_folder = Path(__file__).resolve().parent.parent

features_folder = project_folder / "features" / "model_ready"

X_file = features_folder / "X_features.npy"
y_file = features_folder / "y_labels.npy"


# Step 2: Load features and labels

X = np.load(X_file)
y = np.load(y_file)

print("SCRUM-192: Logistic Regression")
print("Features shape:", X.shape)
print("Labels shape:", y.shape)


# Step 3: Validate the dataset

if X.ndim != 2:
    raise ValueError("Features must be a 2D array")

if len(X) != len(y):
    raise ValueError("Features and labels do not match")

if not np.isfinite(X).all():
    raise ValueError("Features contain invalid values")

if len(np.unique(y)) != 2:
    raise ValueError("Both human and AI-generated labels are required")


# Step 4: Split into training and testing datasets

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# Step 5: Create Logistic Regression model

# Scaling is performed inside the pipeline so the
# scaler is fitted only on training data.

model = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression(
        max_iter=1000,
        random_state=42
    ))
])


# Step 6: Train the model

model.fit(X_train, y_train)

print("\nLogistic Regression training completed.")


# Step 7: Make predictions

predictions = model.predict(X_test)


# Step 8: Evaluate the model

accuracy = accuracy_score(y_test, predictions)

print("\nModel Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")

print(classification_report(
    y_test,
    predictions,
    labels=[0, 1],
    target_names=["Human", "AI-generated"],
    zero_division=0
))

print("\nConfusion Matrix:")

print(confusion_matrix(y_test, predictions, labels=[0, 1]))


# Step 9: Save the trained model

output_folder = project_folder / "models" / "trained"

output_folder.mkdir(parents=True, exist_ok=True)

model_file = output_folder / "logistic_regression.joblib"

joblib.dump(model, model_file)

print("\nModel saved to:", model_file)

print("\nLogistic Regression completed successfully!")