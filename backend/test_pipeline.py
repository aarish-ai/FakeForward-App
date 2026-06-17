import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.extractor import extract_claims
from pipeline.searcher import search_evidence
from pipeline.scorer import score_claim

text = """🚨 IMPORTANT NOTICE: WHATSAPP BECOMING PAID TONIGHT!! 🚨
⚠️ DO NOT IGNORE THIS ⚠️

As of midnight tonight, WhatsApp will stop being free. Due to the massive over-allocation of users on our satellite servers, the CEO of WhatsApp, Dr. Mark Zuckerberg, has announced that the platform is running out of digital space.

Starting tomorrow morning, every message you send will cost $0.05 cents, and pictures will cost $0.10 cents!! 😱😱

HOW TO KEEP YOUR ACCOUNT FREE:
To prove you are an active user and not a bot, you must forward this exact message to at least 10 of your contacts or 3 active groups immediately.

Once you forward this message:

Your WhatsApp logo will turn Bright Pink 🌸

Your account will be verified with a Green Checkmark ✅

Your chats will remain 100% FREE for life!

If you do not forward this message before 11:59 PM tonight, your account will be permanently deactivated and it will cost $49.99 to reactivate it.

Confirmed by the Ministry of Digital Telecommunications and NASA. 🛰️

👇 FORWARD TO 10 PEOPLE NOW TO SAVE YOUR CHATS 👇"""

print("Extracting claims...")
claims = extract_claims(text)
print(f"Extracted {len(claims)} claims.")

for c in claims:
    print(f"\nClaim: {c}")
    evidence = search_evidence(c)
    score = score_claim(c, evidence)
    print(f"Verdict: {score.verdict}, Score: {score.score}")
    print(f"Reason: {score.evidence_summary}")
