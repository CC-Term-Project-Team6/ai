from fastapi import FastAPI
from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.preprocessing import preprocess_text
from app.model import predict_spam
from app.azure_language import analyze_entities
from app.rule_based import rule_based_features, aggregate_result

app = FastAPI(title="Spam/Phishing Detection AI Service")


@app.get("/")
def root():
    return {"message": "AI service is running"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    clean_text = preprocess_text(req.text)

    bert_result = predict_spam(clean_text)

    azure_result = analyze_entities(req.text)

    rule_result = rule_based_features(clean_text)

    final_result = aggregate_result(
        bert_result=bert_result,
        azure_result=azure_result,
        rule_result=rule_result
    )

    return AnalyzeResponse(
        request_id=req.request_id,
        label=final_result["label"],
        risk_level=final_result["risk_level"],
        confidence=final_result["confidence"],
        reason=final_result["reasons"],
        preprocessed_text=clean_text,
        model_outputs={
            "klue_bert": bert_result,
            "azure_language": azure_result,
            "rule_based": rule_result,
            "aggregation_method": "bert_score + rule_bonus + azure_entity_bonus"
        }
    )