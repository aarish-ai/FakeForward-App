import json
import logging
from models import ClaimResult
from pipeline.llm_client import call_llm

logger = logging.getLogger(__name__)

def score_claim(claim: str, evidence: dict) -> ClaimResult:
    """
    Scores the claim based on the evidence.
    Returns early if no evidence is found to save LLM calls.
    """
    wiki_evidence = evidence.get("wikipedia", "")
    ddg_evidence = evidence.get("duckduckgo", [])
    
    # Check if we have any actual evidence
    if not wiki_evidence and not any(ddg_evidence):
        prompt = f"""
        No external search evidence was found for this claim. Using your comprehensive internal knowledge base, assess the factual accuracy of this claim.
        
        Follow these rules:
        1. If you KNOW for a fact that the claim is TRUE and widely documented (e.g. standard features of major apps, known historical events), score it high (80-100) and mark it TRUE.
        2. If the claim contains common hoax/misinformation markers (e.g. fabricated authority figures, technical-sounding nonsense, urgent forward-to-everyone language) AND you know it is not true, score it low (0-20) and mark it FALSE.
        3. Only use UNVERIFIABLE if the claim is highly specific, obscure, or personal and you truly have no knowledge of it.


        Claim: {claim}
        
        Return ONLY a JSON object with:
        - "score": integer from 0 to 100 (0=Completely False, 100=Completely True)
        - "verdict": one of "TRUE", "PROBABLE", "FALSE", or "UNVERIFIABLE"
        - "evidence_summary": a summary of the evidence (max 2 sentences)
        
        Example: {{"score": 10, "verdict": "FALSE", "evidence_summary": "Contains classic hoax markers and fake organization."}}
        """
    else:
        prompt = f"""
        Evaluate the following claim based on the provided evidence AND your comprehensive internal knowledge base.
        If the provided evidence is inconclusive or irrelevant, rely on your internal knowledge to assess the factual accuracy.
        
        Claim: {claim}
        
        Wikipedia Evidence:
        {wiki_evidence if wiki_evidence else "None"}
        
        Other Web Evidence:
        {chr(10).join(ddg_evidence) if ddg_evidence else "None"}
        
        Return ONLY a JSON object with:
        - "score": integer from 0 to 100 (0=Completely False, 100=Completely True)
        - "verdict": one of "TRUE", "PROBABLE", "FALSE", or "UNVERIFIABLE"
        - "evidence_summary": a summary of the evidence (max 2 sentences)
        
        Example: {{"score": 20, "verdict": "FALSE", "evidence_summary": "Evidence shows the claim is inaccurate."}}
        """

    try:
        response_text = call_llm(prompt, expect_json=True)
        try:
            data = json.loads(response_text)
        except json.JSONDecodeError:
            # One repair pass
            repair_prompt = f"""
            Your previous response was not valid JSON. 
            Return ONLY the JSON object, nothing else.
            Previous response:
            {response_text}
            """
            repair_response = call_llm(repair_prompt, expect_json=True)
            data = json.loads(repair_response)
            
        score = data.get("score", 50)
        verdict = data.get("verdict", "UNVERIFIABLE")
        
        # Enforce exact score-to-verdict mapping for UI consistency
        if verdict != "UNVERIFIABLE":
            if score >= 80:
                verdict = "TRUE"
            elif score >= 40:
                verdict = "PROBABLE"
            else:
                verdict = "FALSE"
                
        return ClaimResult(
            claim=claim,
            score=score,
            verdict=verdict,
            evidence_summary=data.get("evidence_summary", "Failed to summarize evidence.")
        )
    except Exception as e:
        logger.error(f"Failed to score claim '{claim}': {e}")
        return ClaimResult(
            claim=claim,
            score=50,
            verdict="UNVERIFIABLE",
            evidence_summary="Scoring failed due to an internal error."
        )
