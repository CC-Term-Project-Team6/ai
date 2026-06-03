def aggregate_result(spam_result, smishing_result, azure_result):
    spam_score = spam_result["spam_score"]
    smishing_score = smishing_result["smishing_score"]

    reasons = []

    risk_entities = azure_result.get("risk_entities", [])

    has_url = False
    has_org = False
    has_phone = False

    for entity in risk_entities:
        category = entity["category"]

        if category == "URL":
            has_url = True
            reasons.append(f"Azure 위험 엔티티 탐지: URL({entity['text']})")

        elif category == "Organization":
            has_org = True
            reasons.append(f"Azure 위험 엔티티 탐지: 기관명({entity['text']})")

        elif category == "PhoneNumber":
            has_phone = True
            reasons.append(f"Azure 위험 엔티티 탐지: 전화번호({entity['text']})")

    adjusted_smishing_score = smishing_score
    adjusted_spam_score = spam_score

    if has_url:
        adjusted_smishing_score += 0.05

    if has_phone:
        adjusted_smishing_score += 0.03

    if has_org:
        adjusted_smishing_score += 0.02

    adjusted_smishing_score = min(adjusted_smishing_score, 1.0)
    adjusted_spam_score = min(adjusted_spam_score, 1.0)

    if adjusted_smishing_score >= 0.70:
        label = "smishing"
        risk_level = "high"
        confidence = adjusted_smishing_score
        reasons.append("AI 모델이 스미싱 패턴을 탐지함")

    elif adjusted_spam_score >= 0.70:
        label = "spam"
        risk_level = "medium"
        confidence = adjusted_spam_score
        reasons.append("AI 모델이 스팸 패턴을 탐지함")

    else:
        label = "normal"
        risk_level = "low"
        confidence = 1 - max(adjusted_spam_score, adjusted_smishing_score)
        reasons.append("특별한 위험 신호 없음")

    return {
        "label": label,
        "risk_level": risk_level,
        "confidence": round(confidence, 4),
        "reasons": reasons
    }