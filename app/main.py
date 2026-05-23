from fastapi import FastAPI
from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.preprocessing import preprocess_text
from app.model import predict_spam

app = FastAPI(title="Spam/Phishing Detection AI Service")


@app.get("/")
def root():
    return {"message": "AI service is running"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    clean_text = preprocess_text(req.text)

    prediction = predict_spam(clean_text)

    return AnalyzeResponse(
        request_id=req.request_id,
        label=prediction["label"],
        risk_level=prediction["risk_level"],
        confidence=prediction["confidence"],
        reason=prediction["reason"],
        preprocessed_text=clean_text,
        model_outputs=prediction["model_outputs"]
    )