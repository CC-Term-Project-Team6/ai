def aggregate_result(model_result, azure_result):
    base_score = model_result["spam_score"]
    final_score = base_score

    reasons = []

    risk_entities = azure_result.get("risk_entities", [])

    for entity in risk_entities:
        category = entity["category"]

        if category == "URL":
            final_score += 0.15
            reasons.append(f"Azure 엔티티 탐지: URL({entity['text']})")

        elif category == "Organization":
            final_score += 0.05
            reasons.append(f"Azure 엔티티 탐지: 기관명({entity['text']})")

        elif category == "PhoneNumber":
            final_score += 0.10
            reasons.append(f"Azure 엔티티 탐지: 전화번호({entity['text']})")

    final_score = min(final_score, 1.0)

    if final_score >= 0.75:
        label = "spam"
        risk_level = "high"
    elif final_score >= 0.45:
        label = "suspicious"
        risk_level = "medium"
    else:
        label = "normal"
        risk_level = "low"

    if not reasons:
        reasons.append("특별한 위험 신호 없음")

    return {
        "label": label,
        "risk_level": risk_level,
        "confidence": round(final_score, 4),
        "reasons": reasons
    }