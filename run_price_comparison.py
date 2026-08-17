# run_price_comparison.py

from src.price_comparator.book_price_checker import collect_book_prices
from src.price_comparator.price_utils import compute_price_stats


def main():
    print("Collecting prices from 3 book pages...\n")

    results = collect_book_prices()

    print("Raw results:")
    for item in results:
        print(f"- {item['site']}")
        print(f"  URL        : {item['url']}")
        print(f"  Raw price  : {item['raw_price']}")
        print(f"  Parsed     : {item['price']}")
        print()

    valid_items = [i for i in results if i["price"] is not None]
    if not valid_items:
        print("No valid prices could be parsed.")
        return

    stats = compute_price_stats(valid_items)

    print("Price statistics:")
    print(f"- Min : {stats['min']}")
    print(f"- Max : {stats['max']}")
    print(f"- Avg : {stats['avg']}")


if __name__ == "__main__":
    main()
