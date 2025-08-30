from typing import Dict, Tuple
import xgboost as xgb
import shap
import numpy as np

# Load model correctly
MODEL_PATH = "models/strategy_predictor.json"
model = xgb.Booster()
model.load_model(MODEL_PATH)

# Define expected feature order
FEATURE_KEYS = ["query_length", "keyword_hits", "avg_steps"]

def predict(features: Dict) -> Tuple[str, str]:
    """
    Predicts strategy outcome using XGBoost and explains it with SHAP.

    Args:
        features (Dict): Feature dictionary from feature_engineer.py

    Returns:
        Tuple[str, str]: (Prediction label, Explanation string)
    """
    # Defensive defaults
    input_vector = [features.get(key, 0) for key in FEATURE_KEYS]
    dmatrix = xgb.DMatrix(np.array([input_vector]), feature_names=FEATURE_KEYS)

    # Predict score
    score = model.predict(dmatrix)[0]

    # Threshold-based label
    if score > 0.7:
        prediction = " High Growth Potential"
    elif score > 0.4:
        prediction = "Moderate Strategic Fit"
    else:
        prediction = " Low Strategic Alignment"

    # SHAP explanation
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(np.array([input_vector]))[0]

    explanation_lines = [f"Prediction: **{prediction}** (Score: {score:.2f})", "", "Feature Contributions:"]
    for key, value, shap_val in zip(FEATURE_KEYS, input_vector, shap_values):
        explanation_lines.append(f" • {key}: {value} → SHAP impact: {shap_val:+.2f}")

    explanation = "\n".join(explanation_lines)
    return prediction, explanation