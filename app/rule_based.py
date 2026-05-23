def rule_based_features(text: str):
    reasons = []
    score_bonus = 0.0

    suspicious_keywords = [
        "인증", "보안", "계정", "정지", "차단", "확인",
        "입금", "결제", "환불", "택배", "국민은행", "카카오",
        "비밀번호", "로그인", "본인확인"
    ]

    for keyword in suspicious_keywords:
        if keyword in text:
            reasons.append(f"의심 키워드 포함: {keyword}")
            score_bonus += 0.05

    if "URL" in text or "http" in text or "www" in text:
        reasons.append("URL 포함")
        score_bonus += 0.15

    score_bonus = min(score_bonus, 0.3)

    return {
        "score_bonus": score_bonus,
        "reasons": reasons
    }


def aggregate_result(bert_result, azure_result, rule_result):
    base_score = bert_result["spam_score"]
    final_score = base_score

    reasons = []

    reasons.extend(rule_result["reasons"])
    final_score += rule_result["score_bonus"]

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