import json
import logging
import re
import requests
from openai import OpenAI
from backend.config import OPENAI_API_KEY, GEMINI_API_KEY, OPENROUTER_API_KEY

logger = logging.getLogger(__name__)

class LLMUnavailableError(Exception):
    """Raised when both primary and fallback LLMs fail."""
    pass

def strip_markdown_code_fences(text: str) -> str:
    """Removes markdown code fences (```json ... ```) from LLM output."""
    text = re.sub(r'^```[a-zA-Z]*\n', '', text.strip())
    text = re.sub(r'\n```$', '', text.strip())
    return text.strip()

import time

def call_llm(prompt: str, expect_json: bool = True) -> str:
    """
    Calls OpenAI GPT-4o as primary via REST API (avoids SDK conflicts),
    falls back to Gemini 2.5 Flash via REST API.
    Includes retry logic for rate limits (429).
    """
    max_retries = 3
    
    # 1. Try OpenAI GPT-4o
    for attempt in range(max_retries):
        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "gpt-4o",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.0
            }
            if expect_json:
                payload["response_format"] = {"type": "json_object"}
                
            res = requests.post(url, headers=headers, json=payload, timeout=15.0)
            
            if res.status_code == 429:
                logger.warning(f"OpenAI 429 Rate Limit. Retrying in {2**attempt}s...")
                time.sleep(2 ** attempt)
                if attempt < max_retries - 1:
                    continue
                    
            res.raise_for_status()
            data = res.json()
            result = data["choices"][0]["message"]["content"]
            
            if expect_json:
                result = strip_markdown_code_fences(result)
            return result
        except Exception as e:
            logger.warning(f"OpenAI GPT-4o failed on attempt {attempt + 1}: {e}")
            if attempt == max_retries - 1:
                break
                
    # 2. Fallback to Gemini via REST API
    for attempt in range(max_retries):
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.0}
            }
            if expect_json:
                payload["generationConfig"]["responseMimeType"] = "application/json"
                
            res = requests.post(url, json=payload, timeout=15.0)
            
            if res.status_code == 429:
                logger.warning(f"Gemini 429 Rate Limit. Retrying in {2**attempt}s...")
                time.sleep(2 ** attempt)
                if attempt < max_retries - 1:
                    continue
                    
            res.raise_for_status()
            data = res.json()
            result = data["candidates"][0]["content"]["parts"][0]["text"]
            
            if expect_json:
                result = strip_markdown_code_fences(result)
            return result
        except Exception as fallback_err:
            logger.warning(f"Gemini failed on attempt {attempt + 1}: {fallback_err}")
            if attempt == max_retries - 1:
                break

    # 3. Fallback to OpenRouter (NVIDIA Nemotron 3 Ultra) via REST API
    for attempt in range(max_retries):
        try:
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
                "messages": [{"role": "user", "content": prompt}],
                "reasoning": {"enabled": True}
            }
            
            res = requests.post(url, headers=headers, json=payload, timeout=20.0)
            
            if res.status_code == 429:
                logger.warning(f"OpenRouter 429 Rate Limit. Retrying in {2**attempt}s...")
                time.sleep(2 ** attempt)
                if attempt < max_retries - 1:
                    continue
                    
            res.raise_for_status()
            data = res.json()
            result = data["choices"][0]["message"]["content"]
            
            if expect_json:
                result = strip_markdown_code_fences(result)
            return result
        except Exception as fallback_err:
            logger.warning(f"OpenRouter failed on attempt {attempt + 1}: {fallback_err}")
            if attempt == max_retries - 1:
                logger.error("All primary and fallback LLMs are unavailable.")
                raise LLMUnavailableError("All primary and fallback LLMs are unavailable.")
