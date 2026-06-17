import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import AnalyzeRequest, AnalyzeResponse, ClaimResult
from pipeline.extractor import extract_claims
from pipeline.searcher import search_evidence
from pipeline.scorer import score_claim
from pipeline.verdict import aggregate_verdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="FakeForward Detector")

# Allow all origins for the hackathon
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    stage_log = []
    
    try:
        # Stage 1: Extract
        stage_log.append("Extracting claims...")
        claims_text = extract_claims(request.text)
        
        if not claims_text:
            return AnalyzeResponse(
                claims=[],
                overall_verdict="NO_CLAIMS_FOUND",
                overall_score=50,
                stage_log=stage_log + ["Analysis complete: No checkable claims found."]
            )
            
        import time
        # Stage 2 & 3: Search and Score
        stage_log.append("Searching evidence and scoring...")
        results = []
        for claim in claims_text:
            evidence = search_evidence(claim)
            result = score_claim(claim, evidence)
            results.append(result)
            # Sleep briefly to avoid Gemini free-tier rate limits (15 RPM)
            time.sleep(3)
            
        # Stage 4: Aggregate Verdict
        stage_log.append("Aggregating overall verdict...")
        overall_verdict, overall_score = aggregate_verdict(results)
        
        stage_log.append("Analysis complete.")
        
        return AnalyzeResponse(
            claims=results,
            overall_verdict=overall_verdict,
            overall_score=overall_score,
            stage_log=stage_log
        )
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        # Ensure raw traceback doesn't reach the frontend
        raise HTTPException(status_code=500, detail="An internal error occurred while processing the request.")

from fastapi.staticfiles import StaticFiles
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
