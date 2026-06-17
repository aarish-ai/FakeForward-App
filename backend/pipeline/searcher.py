import logging
import requests
from duckduckgo_search import DDGS
from typing import Dict, List

logger = logging.getLogger(__name__)

def search_evidence(claim: str) -> Dict[str, str | List[str]]:
    """
    Searches Wikipedia and DuckDuckGo for evidence regarding the claim.
    Returns {"wikipedia": str, "duckduckgo": list[str]}.
    """
    evidence = {
        "wikipedia": "",
        "duckduckgo": []
    }
    
    print(f"\n[DEBUG] Searching for claim: {claim}")
    
    # 1. Wikipedia search
    try:
        # We use the search API because exact title matches are rare.
        # We take the first result and fetch its summary.
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={requests.utils.quote(claim)}&utf8=&format=json"
        headers = {"User-Agent": "FakeForwardDetector/1.0 (test@example.com)"}
        search_res = requests.get(search_url, headers=headers, timeout=5.0)
        search_res.raise_for_status()
        search_data = search_res.json()
        
        search_results = search_data.get("query", {}).get("search", [])
        if search_results:
            first_title = search_results[0]["title"]
            summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(first_title)}"
            summary_res = requests.get(summary_url, headers=headers, timeout=5.0)
            if summary_res.status_code == 200:
                summary_data = summary_res.json()
                evidence["wikipedia"] = summary_data.get("extract", "")
        else:
            logger.warning(f"Wikipedia returned zero results for claim '{claim}'")
    except Exception as e:
        logger.warning(f"Wikipedia search failed for claim '{claim}': {e}")

    # 2. DuckDuckGo search (wrapped to catch ALL exceptions)
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(claim, max_results=3))
            if not results:
                logger.warning(f"DuckDuckGo returned zero results for claim '{claim}'")
            evidence["duckduckgo"] = [r.get("body", "") for r in results]
    except Exception as e:
        logger.warning(f"DuckDuckGo search failed for claim '{claim}': {type(e).__name__}: {e}")
        
    return evidence
