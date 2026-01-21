import requests


def run_subdomain_enum(domain, logger=None):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        if logger:
            logger.error(f"crt.sh request failed: {e}")
        return []

    try:
        data = response.json()
    except Exception:
        if logger:
            logger.error("Failed to parse crt.sh response")
        return []

    subdomains = set()

    for entry in data:
        name = entry.get("name_value", "")
        for sub in name.split("\n"):
            if sub.endswith(domain):
                subdomains.add(sub.strip())

    if logger:
        logger.info(f"Found {len(subdomains)} subdomains")

    return sorted(subdomains)
