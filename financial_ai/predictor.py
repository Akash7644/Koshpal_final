import joblib
import pandas as pd
from pathlib import Path


# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Model directory
MODEL_DIR = PROJECT_ROOT / "models"


# Load trained model artifacts
pipeline = joblib.load(
    MODEL_DIR / "final_xgboost_pipeline.pkl"
)

final_features = joblib.load(
    MODEL_DIR / "final_features.pkl"
)

target_encoder = joblib.load(
    MODEL_DIR / "target_encoder.pkl"
)


def predict_financial_health(employee_data):

    # Convert employee input into DataFrame
    employee_df = pd.DataFrame([employee_data])

    # Check required features
    missing_features = [
        feature
        for feature in final_features
        if feature not in employee_df.columns
    ]

    if missing_features:
        raise ValueError(
            f"Missing required features: {missing_features}"
        )

    # Keep only the features used during training
    employee_df = employee_df[final_features]

    # Predict class
    prediction = pipeline.predict(employee_df)[0]

    # Get class probabilities
    probabilities = pipeline.predict_proba(employee_df)[0]

    # Convert encoded prediction to original label
    predicted_class = target_encoder.inverse_transform(
        [[prediction]]
    )[0][0]

    # Highest probability = confidence
    confidence = float(probabilities.max())

    # Map probabilities to class names
    class_probabilities = {
        str(class_name): float(probability)
        for class_name, probability
        in zip(target_encoder.classes_, probabilities)
    }

    return {
        "prediction": str(predicted_class),
        "confidence": confidence,
        "probabilities": class_probabilities
    }