from pathlib import Path

# DNS Configuration

DNS_TIMEOUT = 3
DNS_RETRIES = 2
DNS_RECORD_TYPES = ["A", "MX", "TXT", "NS"]

# Output Configuration

BASE_OUTPUT_DIR = Path("output")
RAW_OUTPUT_DIR = BASE_OUTPUT_DIR / "raw"
REPORT_OUTPUT_DIR = BASE_OUTPUT_DIR / "reports"

# Reporting Configuration

DEFAULT_REPORT_FORMAT = "txt"


