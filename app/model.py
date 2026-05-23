from app.rule_based import rule_based_predict
from app.azure_language import analyze_entities


def predict_spam(text: str):
    label, risk_level, confidence, reasons = rule_based_predict(text)

    azure_result = analyze_entities(text)

    suspicious_entities = []

    for entity in azure_result.get("entities", []):
        if entity["category"] in ["URL", "Organization", "PhoneNumber", "Email"]:
            suspicious_entities.append(entity)

    if suspicious_entities:
        reasons.append("Azure AI Language에서 의심 엔티티 탐지")
        confidence = min(confidence + 0.05, 0.99)

    return {
        "label": label,
        "risk_level": risk_level,
        "confidence": confidence,
        "reason": reasons,
        "model_outputs": {
            "rule_based": {
                "label": label,
                "confidence": confidence
            },
            "azure_language": azure_result
        }
    }
