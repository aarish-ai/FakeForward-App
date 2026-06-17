import os
import sys

# Ensure backend directory is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.extractor import extract_claims
from pipeline.searcher import search_evidence
from pipeline.scorer import score_claim

tests = [
    {
        "name": "1. Hoax Message",
        "message": """🚨🚨 URGENT NOTICE: DO NOT OPEN "⚡BLUE LIGHT" VIDEO!! 🚨🚨
The World Cyber Security Organization (WCSO) in Geneva issued a red alert...
hacker group circulating a video called "Blue Light 2026"...
Your phone will freeze instantly within 10 seconds, formats your entire hard
drive, steals bank OTPs, can cause the battery to explode...
BBC and CNN confirmed this... — Dr. Rahul Sharma, Senior Vice President of
Cyber NASA..."""
    },
    {
        "name": "2. Real, True, Checkable Fact",
        "message": "The Eiffel Tower is located in Paris, France, and was completed in 1889."
    },
    {
        "name": "3. Obscure but Plausible",
        "message": "The annual Springfield Community Bake Sale of 2023 raised exactly $420 for the local dog shelter, according to the neighborhood newsletter."
    }
]

import time

for test in tests:
    print(f"\n{'='*50}\nRUNNING TEST: {test['name']}\n{'='*50}")
    claims = extract_claims(test["message"])
    for claim in claims:
        print(f"\n--- Processing Claim: {claim} ---")
        evidence = search_evidence(claim)
        
        score = score_claim(claim, evidence)
        print(f"Verdict: {score.verdict}, Score: {score.score}")
        print(f"Reason: {score.evidence_summary}")
        time.sleep(3)
