import json
import logging
from typing import List
from pipeline.llm_client import call_llm

logger = logging.getLogger(__name__)

def extract_claims(text: str) -> List[str]:
    """
    Extracts up to 5 objective, checkable factual claims from the text.
    Ignores opinions, jokes, and rhetorical questions.
    Returns an empty list if no claims are found or if LLMs fail completely.
    """
    prompt = f"""
    Analyze the following text. Extract up to 5 objective, checkable factual claims from it.
    Do NOT include opinions, jokes, or rhetorical questions.
    Return ONLY a JSON object with the key "claims" containing a list of strings.
    Example: {{"claims": ["The sky is blue", "Water boils at 100 degrees Celsius"]}}
    
    Text:
    {text}
    """
    
    try:
        response_text = call_llm(prompt, expect_json=True)
        try:
            data = json.loads(response_text)
            return data.get("claims", [])[:5]
        except json.JSONDecodeError:
            # One repair pass
            repair_prompt = f"""
            Your previous response was not valid JSON. 
            Return ONLY the JSON object `{{\"claims\": [...]}}`, nothing else.
            Previous response:
            {response_text}
            """
            repair_response = call_llm(repair_prompt, expect_json=True)
            data = json.loads(repair_response)
            return data.get("claims", [])[:5]
    except Exception as e:
        logger.error(f"Failed to extract claims: {e}")
        # Return empty list rather than crashing, the API layer will handle it gracefully
        return []
