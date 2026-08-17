# tests/test_price_utils.py

from src.price_comparator.price_utils import parse_price_to_float, compute_price_stats


def test_parse_price_to_float_examples():
    assert parse_price_to_float("₺34.999,90") == 34999.90
    assert parse_price_to_float("34,999.90 TL") == 34999.90
    assert parse_price_to_float("1999") == 1999.0


def test_compute_price_stats():
    items = [
        {"site": "A", "price": 100.0},
        {"site": "B", "price": 200.0},
        {"site": "C", "price": 300.0},
    ]
    stats = compute_price_stats(items)
    assert stats["min"] == 100.0
    assert stats["max"] == 300.0
    assert stats["avg"] == 200.0
