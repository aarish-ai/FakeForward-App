import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.pipeline.scorer import score_claim

claim1 = "Cybercriminals are using 'verification code scams' to steal WhatsApp accounts."
claim2 = "WhatsApp has a built-in feature called Two-Step Verification."
claim3 = "Two-Step Verification requires a 6-digit PIN."

# Simulate Wikipedia returning a general summary for 'WhatsApp' instead of the specific feature
evidence = {
    "wikipedia": "WhatsApp Messenger is a freeware, cross-platform, centralized instant messaging and voice-over-IP service owned by Meta.", 
    "duckduckgo": []
}

for claim in [claim1, claim2, claim3]:
    print(f"\nClaim: {claim}")
    result = score_claim(claim, evidence)
    print(f"Verdict: {result.verdict}")
    print(f"Score: {result.score}")
    print(f"Reason: {result.evidence_summary}")
