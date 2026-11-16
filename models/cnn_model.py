from pathlib import Path

import numpy as np
import pandas as pd
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Conv2D, Dense, Dropout, Flatten, MaxPooling2D
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.optimizers import Adam


# Input settings
feature_height = 100
feature_width = 13
feature_channels = 1
epochs = 50
batch_size = 32
learning_rate = 0.001
random_seed = 42
validation_fraction = 0.2

# File paths
project_root = Path(__file__).resolve().parent.parent
features_path = project_root / "features" / "prepared" / "prepared_features.npy"
labels_path = project_root / "dataset" / "labels.csv"
output_folder = project_root / "models" / "output"
model_path = output_folder / "cnn_model.keras"
results_path = output_folder / "cnn_training_results.csv"


def build_cnn_model():
    model = Sequential(
        [
            Conv2D(
                filters=32,
                kernel_size=(3, 3),
                activation="relu",
                padding="same",
                input_shape=(feature_height, feature_width, feature_channels),
            ),
            MaxPooling2D(pool_size=(2, 2)),
            Conv2D(
                filters=64,
                kernel_size=(3, 3),
                activation="relu",
                padding="same",
            ),
            MaxPooling2D(pool_size=(2, 2)),
            Flatten(),
            Dense(units=64, activation="relu"),
            Dropout(0.5),
            Dense(1, activation="sigmoid"),
        ]
    )
    model.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss="binary_crossentropy",
        metrics=["accuracy"],
    )
    return model


def load_training_data():
    features = np.load(features_path)
    labels_frame = pd.read_csv(labels_path)

    if "encodedLabel" in labels_frame.columns:
        labels = labels_frame["encodedLabel"].to_numpy()
    elif "label" in labels_frame.columns:
        label_mapping = {"human": 0, "ai_generated": 1}
        labels = labels_frame["label"].map(label_mapping).to_numpy()
        if pd.isna(labels).any():
            unknown_labels = labels_frame.loc[
                pd.isna(labels), "label"
            ].unique()
            raise ValueError(f"Unknown labels in {labels_path}: {unknown_labels}")
    else:
        raise ValueError(
            f"{labels_path} must contain an 'encodedLabel' or 'label' column"
        )

    if features.ndim == 3:
        features = features[..., np.newaxis]
    expected_shape = (feature_height, feature_width, feature_channels)
    if features.ndim != 4 or features.shape[1:] != expected_shape:
        raise ValueError(
            f"Expected features with shape (samples, {expected_shape}), "
            f"got {features.shape}"
        )
    if not np.isfinite(features).all():
        raise ValueError(f"Non-finite feature values found in {features_path}")
    if len(features) != len(labels):
        raise ValueError(
            f"Feature/label count mismatch: {len(features)} features in "
            f"{features_path}, but {len(labels)} labels in {labels_path}"
        )

    try:
        labels = pd.to_numeric(pd.Series(labels), errors="raise").to_numpy()
    except (TypeError, ValueError) as error:
        raise ValueError("Labels must be encoded as integers 0 or 1") from error
    if not np.isfinite(labels).all() or not np.isin(labels, [0, 1]).all():
        raise ValueError("Labels must be encoded as integers 0 or 1")
    labels = labels.astype(np.int64)

    rng = np.random.default_rng(random_seed)
    train_indices = []
    validation_indices = []
    for label in (0, 1):
        class_indices = np.flatnonzero(labels == label)
        if len(class_indices) < 2:
            raise ValueError(
                "At least two examples of each label are required for a "
                "stratified train/validation split"
            )
        rng.shuffle(class_indices)
        validation_count = min(
            max(1, round(len(class_indices) * validation_fraction)),
            len(class_indices) - 1,
        )
        validation_indices.extend(class_indices[:validation_count])
        train_indices.extend(class_indices[validation_count:])

    rng.shuffle(train_indices)
    rng.shuffle(validation_indices)
    X_train = features[train_indices]
    Y_train = labels[train_indices]
    X_val = features[validation_indices]
    Y_val = labels[validation_indices]

    print("CNN training features shape:", X_train.shape)
    print("CNN validation features shape:", X_val.shape)
    print("CNN training labels shape:", Y_train.shape)
    print("CNN validation labels shape:", Y_val.shape)

    return X_train, Y_train, X_val, Y_val


def train_cnn_model():
    X_train, Y_train, X_val, Y_val = load_training_data()
    model = build_cnn_model()

    early_stopping = EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True,
    )
    history = model.fit(
        X_train,
        Y_train,
        validation_data=(X_val, Y_val),
        epochs=epochs,
        batch_size=batch_size,
        callbacks=[early_stopping],
        verbose=1,
    )
    return model, history


def save_training_results(history):
    output_folder.mkdir(parents=True, exist_ok=True)
    results = pd.DataFrame(history.history)
    results.to_csv(results_path, index=False)
    print(f"Saved CNN training results to {results_path}")


def save_training_model(model):
    output_folder.mkdir(parents=True, exist_ok=True)
    model.save(model_path)
    print(f"Saved CNN model to {model_path}")


if __name__ == "__main__":
    model, history = train_cnn_model()
    save_training_results(history)
    save_training_model(model)

    reloaded_model = load_model(model_path)
    print("CNN model successfully reloaded")
    reloaded_model.summary()
