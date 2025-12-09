"""
api.py

Functions for building API URL and fetching exchange
rate data.

Public functions:
- load_api_key_from_env() -> str
- make_url(api_key: str, base: str = "USD") -> str
- fetch_rates(api_key: str, base: str = "USD", timeout:
int = 10, retries: int = 2) -> dict
"""

from typing import Optional
import os
import time
import logging
import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

BASE_URL = "https://v6.exchangerate-api.com/v6"

def load_api_key_from_env(env_name: str = "API_KEY") -> Optional[str]:
    """
    Read API key from environment variable

    Returns:
    api_key (str) if set, otherwise None.
    """
    load_dotenv()
    return os.getenv(env_name)

def make_url(api_key: str, base: str = "USD") -> str:
    """
    Build the exchangerate-api URL for a given api_key
    and base currency

    """
    return f"{BASE_URL}/{api_key}/latest/{base}"

def fetch_rates(api_key: str, base: str = "USD", timeout: int = 10, retries: int = 2) -> dict:
    """
    Fetch exchange rates JSON from exchangerate-api.

    Prarmeters:
    api_key: API key string (must be valid)
    base: base currency code (e.g., "USD")
    timeout: request timeout in seconds
    retries: number of retries on transient errors (0 => no try)

    Returns:
        Parsed JSON (dict) on success.

    Raises:
        requests.exeptions.RequestsException for network/HTTP errors.
        ValueError if response cannot be parsed as JSON or API returned an error

    """
    if not api_key:
        raise ValueError("API key is empty")
    
    url = make_url(api_key, base)
    attempt = 0
    last_exc = None

    while attempt <= retries:
        try:
            logger.info("Requesting exchange rates (attempt %d): %s", attempt + 1, url)
            resp = requests.get(url, timeout=timeout)
            resp.raise_for_status()
            data = resp.json()  # may raise ValueError
            #Basic validation: ensure result == 'success' and conversion_rates exist
            if data.get("result") != "success":
                err_type = data.get("error-type", "unknown")
                raise ValueError(f"API returned non-success result: {err_type}")
            if 'conversion_rates' not in data:
                raise ValueError("API response missing 'conversion_rate' field")
            return data
        except requests.exceptions.RequestException as e:
            logger.warning("Network/HTTP error while fetching rates: %s", e)
            last_exc = e
            attempt += 1
            time.sleep(1)  #brief backoff
        except ValueError as e:
            # JSON parse error or API logical error - do not retry
            logger.error("Invalid API response: %s", e)
            raise

    # if we exhausted retries, raise last network exception
    logger.error("Failed to fetch rates after %d attempts", retries + 1)
    raise last_exc if last_exc is not None else RuntimeError("Unknown fetch error")