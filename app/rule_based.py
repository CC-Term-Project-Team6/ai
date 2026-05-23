def rule_based_predict(text: str):
    keywords = ["인증", "계좌", "비밀번호", "택배", "보안", "확인", "결제", "차단"]

    score = 0
    reasons = []

    for word in keywords:
        if word in text:
            score += 1
            reasons.append(f"의심 키워드 포함: {word}")

    if "__URL__" in text:
        score += 2
        reasons.append("URL 포함")

    if score >= 4:
        return "spam", "high", 0.9, reasons
    elif score >= 2:
        return "suspicious", "medium", 0.75, reasons
    else:
        return "normal", "low", 0.55, ["위험 요소가 적음"]
