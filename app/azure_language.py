import os
from dotenv import load_dotenv
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()


def get_language_client():
    endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
    key = os.getenv("AZURE_LANGUAGE_KEY")

    if not endpoint or not key:
        return None

    return TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )


def analyze_entities(text: str):
    client = get_language_client()

    if client is None:
        return {
            "enabled": False,
            "entities": [],
            "error": "Azure Language endpoint/key not configured"
        }

    try:
        result = client.recognize_entities([text], language="ko")[0]

        if result.is_error:
            return {
                "enabled": True,
                "entities": [],
                "error": str(result.error)
            }

        entities = []
        for entity in result.entities:
            entities.append({
                "text": entity.text,
                "category": entity.category,
                "subcategory": entity.subcategory,
                "confidence_score": entity.confidence_score
            })

        return {
            "enabled": True,
            "entities": entities,
            "error": None
        }

    except Exception as e:
        return {
            "enabled": True,
            "entities": [],
            "error": str(e)
        }