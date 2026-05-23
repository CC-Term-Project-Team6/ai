from fastapi import FastAPI
from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.preprocessing import preprocess_text
from app.model import predict_spam
from app.azure_language import analyze_entities
from app.rule_based import rule_based_features
from app.aggregator import aggregate_result
import logging

app = FastAPI(title="Spam/Phishing Detection AI Service")

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

@app.get("/")
def root():
    return {"message": "AI service is running"}

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):

    logger.info(f"Request received: {req.request_id}")

    clean_text = preprocess_text(req.text)

    logger.info(f"Preprocessed text: {clean_text}")

    model_result = predict_spam(clean_text)

    logger.info(f"Model result: {model_result}")

    azure_result = analyze_entities(req.text)

    logger.info(f"Azure result: {azure_result}")

    rule_result = rule_based_features(clean_text)

    logger.info(f"Rule result: {rule_result}")

    final_result = aggregate_result(
        model_result=model_result,
        azure_result=azure_result,
        rule_result=rule_result
    )

    logger.info(f"Final aggregation: {final_result}")

    return AnalyzeResponse(
        request_id=req.request_id,
        label=final_result["label"],
        risk_level=final_result["risk_level"],
        confidence=final_result["confidence"],
        reason=final_result["reasons"],
    )