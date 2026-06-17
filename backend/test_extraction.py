import os
import sys
import logging

# Ensure backend directory is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Enable logging to see the exception if any
logging.basicConfig(level=logging.DEBUG)

from pipeline.extractor import extract_claims

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

print("Running extraction...")
claims = extract_claims(text)
print("Result:")
print(claims)
