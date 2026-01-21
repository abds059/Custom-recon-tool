import whois

def run_whois_lookup(domain, logger=None):
    try:
        w = whois.whois(domain)
    except Exception as e:
        if logger:
            logger.error(f"WHOIS lookup failed: {e}")
        return {}

    result = {
        "domain_name": w.domain_name,
        "registrar": w.registrar,
        "creation_date": str(w.creation_date),
        "expiration_date": str(w.expiration_date),
        "name_servers": w.name_servers,
    }

    if logger:
        logger.info("WHOIS lookup completed")

    return result
