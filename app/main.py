from fastapi import FastAPI
from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.preprocessing import preprocess_text
from app.rule_based import rule_based_predict

app = FastAPI(title="Spam/Phishing Detection AI Service")


@app.get("/")
def root():
    return {"message": "AI service is running"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    clean_text = preprocess_text(req.text)

    label, risk_level, confidence, reasons = rule_based_predict(clean_text)

    return AnalyzeResponse(
        request_id=req.request_id,
        label=label,
        risk_level=risk_level,
        confidence=confidence,
        reason=reasons,
        preprocessed_text=clean_text,
        model_outputs={
            "method": "rule_based_v0"
        }
    )
