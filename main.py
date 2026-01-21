import argparse
import json
from datetime import datetime, timezone

from logger import get_logger
from dispatcher import dispatch
from config import RAW_OUTPUT_DIR, REPORT_OUTPUT_DIR
from reporting import generate_reports


def parse_args():
    parser = argparse.ArgumentParser(
        description="Custom Recon Tool"
    )

    parser.add_argument("domain", help="Target domain")

    # Passive recon
    parser.add_argument("--dns", action="store_true", help="Run DNS enumeration")
    parser.add_argument("--subdomains", action="store_true", help="Run subdomain enumeration (crt.sh)")
    parser.add_argument("--whois", action="store_true", help="Run WHOIS lookup")

    # Active recon
    parser.add_argument("--portscan", action="store_true", help="Run port scan")

    # Verbosity
    parser.add_argument(
        "-v", "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (-v, -vv)"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    logger = get_logger(args.verbose)
    logger.info("Recon tool started")

    # Ensure output directories exist
    RAW_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Dispatch enabled modules
    results = dispatch(args, logger)

    # Save raw results
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    output_file = RAW_OUTPUT_DIR / f"{args.domain}_{timestamp}.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    logger.info(f"Raw results saved to {output_file}")

    generate_reports(
        args.domain,
        results,
        REPORT_OUTPUT_DIR,
        logger
    )

    logger.info("Recon tool finished")

if __name__ == "__main__":
    main()
