from typing import Dict, Tuple
import xgboost as xgb
import shap
import numpy as np

# Model path and feature schema
MODEL_PATH = "models/strategy_predictor.json"
FEATURE_KEYS = ["query_length", "keyword_hits", "avg_steps"]

# Load model safely
try:
    model = xgb.Booster()
    model.load_model(MODEL_PATH)
except Exception as e:
    print(f"⚠️ Failed to load model: {e}")
    model = None  # You can trigger fallback here if needed

def predict(features: Dict) -> Tuple[str, str]:
    """
    Predicts strategy outcome using XGBoost and explains it with SHAP.

    Args:
        features (Dict): Feature dictionary from feature_engineer.py

    Returns:
        Tuple[str, str]: (Prediction label, Explanation string)
    """
    # Defensive feature vector
    input_vector = [features.get(key, 0) for key in FEATURE_KEYS]
    dmatrix = xgb.DMatrix(np.array([input_vector]), feature_names=FEATURE_KEYS)

    # Predict score
    try:
        score = model.predict(dmatrix)[0]
    except Exception as e:
        return "⚠️ Prediction Failed", f"Model error: {e}"

    # Threshold-based label
    if score > 0.7:
        prediction = "📈 High Growth Potential"
    elif score > 0.4:
        prediction = "📊 Moderate Strategic Fit"
    else:
        prediction = "⚠️ Low Strategic Alignment"

    # SHAP explanation
    try:
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(np.array([input_vector]))[0]

        explanation_lines = [
            f"Prediction: **{prediction}** (Score: {score:.2f})",
            "",
            "🔍 Feature Contributions:"
        ]
        for key, value, shap_val in zip(FEATURE_KEYS, input_vector, shap_values):
            explanation_lines.append(f" • {key}: {value} → SHAP impact: {shap_val:+.2f}")

        explanation = "\n".join(explanation_lines)

    except Exception as e:
        explanation = (
            f"Prediction: **{prediction}** (Score: {score:.2f})\n\n"
            f"⚠️ SHAP explanation unavailable due to error: {e}"
        )

    return prediction, explanation