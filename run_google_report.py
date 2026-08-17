# run_google_report.py

from src.google_report.report_generator import build_keyword_report, export_report_to_pdf


def main():
    keyword = input("Enter a keyword for web report: ")
    report = build_keyword_report(keyword, max_results=5)

    # Print a short summary to the console
    print(f"\n=== Report for keyword: {report['keyword']} ===\n")
    for i, entry in enumerate(report["entries"], start=1):
        print(f"Source {i}: {entry['url']}")
        print(entry["summary"])
        print("-" * 80)

    print("\nConclusion:")
    print(report["conclusion"])

    # Save the report as a PDF
    export_report_to_pdf(report, f"report_{keyword.replace(' ', '_')}.pdf")
    print("\nPDF report exported.")


if __name__ == "__main__":
    main()
