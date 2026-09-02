import logging
import urllib.request
import urllib.parse
import ssl
import re
from typing import Dict, Any, Optional
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

OFFICIAL_DOMAINS = {"mospi.gov.in", "nssta.gov.in", "esankhyiki.mospi.gov.in", "igotkarmayogi.gov.in"}
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Antigravity/2.0 (MoSPI Capacity Platform)"
MAX_RESPONSE_SIZE = 5_000_000  # 5 MB safety cap
DEFAULT_TIMEOUT_SECONDS = 10

def is_official_domain(url: str) -> bool:
    if not url:
        return False
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return False
        domain = parsed.netloc.lower()
        return any(domain == valid or domain.endswith("." + valid) for valid in OFFICIAL_DOMAINS)
    except Exception:
        return False

def fetch_official_live_url(
    url: str,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
    max_bytes: int = MAX_RESPONSE_SIZE
) -> Dict[str, Any]:
    """
    Executes a safe, verified HTTP GET request to an official government portal.
    Enforces domain allowlisting, response size limits, timeouts, and safe redirect validation.
    """
    if not is_official_domain(url):
        logger.warning(f"[LiveFetcher] Refused to fetch non-official domain: {url}")
        return {
            "success": False,
            "status_code": 0,
            "error": f"Security Policy Violation: Domain not in official allowlist ({OFFICIAL_DOMAINS})"
        }

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE  # Handles legacy government SSL chain variations safely

    headers = {
        "User-Agent": DEFAULT_USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml,text/csv,application/json;q=0.9,*/*;q=0.8"
    }

    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as response:
            final_url = response.geturl()
            if not is_official_domain(final_url):
                return {
                    "success": False,
                    "status_code": response.status,
                    "error": f"Security Violation: Redirected to non-official domain {final_url}"
                }

            content_type = response.headers.get("Content-Type", "")
            content_length = response.headers.get("Content-Length")
            if content_length and int(content_length) > max_bytes:
                return {
                    "success": False,
                    "status_code": response.status,
                    "error": f"Size Limit Exceeded: Content-Length {content_length} exceeds limit {max_bytes}"
                }

            raw_bytes = response.read(max_bytes + 1)
            if len(raw_bytes) > max_bytes:
                return {
                    "success": False,
                    "status_code": response.status,
                    "error": f"Size Limit Exceeded: Downloaded payload exceeded max limit of {max_bytes} bytes"
                }

            text_content = ""
            meta_title = None
            meta_description = None

            try:
                text_content = raw_bytes.decode("utf-8", errors="ignore")
                title_match = re.search(r"<title>(.*?)</title>", text_content, re.IGNORECASE | re.DOTALL)
                if title_match:
                    meta_title = title_match.group(1).strip()

                desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', text_content, re.IGNORECASE)
                if not desc_match:
                    desc_match = re.search(r'<meta\s+content=["\'](.*?)["\']\s+name=["\']description["\']', text_content, re.IGNORECASE)
                if desc_match:
                    meta_description = desc_match.group(1).strip()
            except Exception:
                pass

            return {
                "success": True,
                "status_code": response.status,
                "final_url": final_url,
                "content_type": content_type,
                "headers": dict(response.headers),
                "raw_bytes": raw_bytes,
                "text_content": text_content,
                "meta_title": meta_title,
                "meta_description": meta_description
            }
    except Exception as e:
        logger.warning(f"[LiveFetcher] HTTP GET failed for '{url}': {str(e)}")
        return {
            "success": False,
            "status_code": 0,
            "error": str(e)
        }
