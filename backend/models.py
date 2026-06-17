from pydantic import BaseModel, Field
from typing import List

class AnalyzeRequest(BaseModel):
    # Reject anything over 3000 chars to prevent token exhaustion
    text: str = Field(..., max_length=3000)

class ClaimResult(BaseModel):
    claim: str
    score: int
    verdict: str
    evidence_summary: str

class AnalyzeResponse(BaseModel):
    claims: List[ClaimResult]
    overall_verdict: str
    overall_score: int
    stage_log: List[str]
