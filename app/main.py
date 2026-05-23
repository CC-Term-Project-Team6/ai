from fastapi import FastAPI
from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.preprocessing import preprocess_text
from app.model import predict_spam
from app.azure_language import analyze_entities
from app.rule_based import rule_based_features
from app.aggregator import aggregate_result
import logging
import asyncio

app = FastAPI(title="Spam/Phishing Detection AI Service")

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

@app.get("/")
def root():
    return {"message": "AI service is running"}

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(req: AnalyzeRequest):

    clean_text = preprocess_text(req.text)

    model_task = asyncio.to_thread(
        predict_spam,
        clean_text
    )

    azure_task = asyncio.to_thread(
        analyze_entities,
        req.text
    )

    model_result, azure_result = await asyncio.gather(
        model_task,
        azure_task
    )

    rule_result = rule_based_features(clean_text)

    final_result = aggregate_result(
        model_result=model_result,
        azure_result=azure_result,
        rule_result=rule_result
    )

    logger.info(
        f"""
[ANALYZE RESULT]
request_id={req.request_id}

clean_text={clean_text}

model_result={model_result}

azure_result={azure_result}

rule_result={rule_result}

final_result={final_result}
"""
    )

    return AnalyzeResponse(
        request_id=req.request_id,
        label=final_result["label"],
        risk_level=final_result["risk_level"],
        confidence=final_result["confidence"],
        reason=final_result["reasons"],
    )