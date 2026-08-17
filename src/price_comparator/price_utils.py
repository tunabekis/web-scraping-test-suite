# src/price_comparator/price_utils.py

from typing import List, Dict
import re
from statistics import mean


def parse_price_to_float(price_str: str) -> float:
    """
    Parses price strings such as '₺34.999,90', '34,999.90 TL' or '£51.77'
    into a float. Kept intentionally general to handle a variety of
    currency symbols and thousands/decimal separator conventions.
    """
    if not price_str:
        raise ValueError("Empty price string")

    cleaned = price_str.strip()

    # Strip known currency symbols/codes.
    for token in ["TL", "TRY", "₺", "$", "€", "£"]:
        cleaned = cleaned.replace(token, "")

    # Remove whitespace.
    cleaned = cleaned.replace(" ", "")

    # If both '.' and ',' are present, the rightmost one is treated as the
    # decimal separator. Example: 34.999,90 -> 34999.90
    if "," in cleaned and "." in cleaned:
        if cleaned.rfind(",") > cleaned.rfind("."):
            cleaned = cleaned.replace(".", "")
            cleaned = cleaned.replace(",", ".")
    else:
        # Only a comma present -> treat it as a decimal separator.
        if "," in cleaned:
            cleaned = cleaned.replace(",", ".")

    # Keep only digits and the decimal point.
    cleaned = re.sub(r"[^0-9.]", "", cleaned)

    # Safety net: if multiple dots remain, treat the last one as decimal.
    if cleaned.count(".") > 1:
        whole = cleaned.replace(".", "")
        cleaned = whole[:-2] + "." + whole[-2:]

    return float(cleaned)


def compute_price_stats(price_items: List[Dict]) -> Dict[str, float]:
    """
    price_items: [ { "site": "...", "price": 34999.0 }, ... ]

    Returns:
        {
            "min":  ...,
            "max":  ...,
            "avg":  ...
        }
    """
    if not price_items:
        raise ValueError("No price items provided")

    prices = [item["price"] for item in price_items if item.get("price") is not None]
    if not prices:
        raise ValueError("No valid prices found")

    return {
        "min": min(prices),
        "max": max(prices),
        "avg": mean(prices),
    }
