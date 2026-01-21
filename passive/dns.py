import dns.resolver 
import dns.exception
from datetime import datetime

from config import DNS_TIMEOUT, DNS_RETRIES, DNS_RECORD_TYPES

def run_dns_enum (domain: str, logger):

    logger.info(f"Starting DNS enumeration for {domain}")

    resolver = dns.resolver.Resolver()
    resolver.timeout =  DNS_TIMEOUT
    resolver.lifetime = DNS_TIMEOUT * DNS_RETRIES

    results = {
        "domain": domain,
        "records": {
            "A": [],
            "MX": [],
            "TXT": [],
            "NS": []
        },
        "errors": [],
        "metadata": {
            "started_at": datetime.utcnow().isoformat() + "Z",
            "finished_at": None
        }

    }

    for record_type in DNS_RECORD_TYPES:
        try:
            logger.debug(f"Querying {record_type} records")

            answers = resolver.resolve(domain, record_type)

            if record_type == "A":
                for rdata in answers:
                    results["records"]["A"].append(str(rdata))

            elif record_type == "MX":
                for rdata in answers:
                    results["records"]["MX"].append({
                        "priority": rdata.preference,
                        "exchange": str(rdata.exchange).rstrip(".")
                    })

            elif record_type == "TXT":
                for rdata in answers:
                    txt_value = "".join(
                        part.decode() if isinstance(part, bytes) else part
                        for part in rdata.strings
                    )
                    results["records"]["TXT"].append(txt_value)

            elif record_type == "NS":
                for rdata in answers:
                    results["records"]["NS"].append(
                        str(rdata.target).rstrip(".")
                    )

        except dns.resolver.NoAnswer:
            logger.debug(f"No {record_type} records found")
        
        except dns.resolver.NXDOMAIN:
            logger.error("Domain doesnot exist")
            results["errors"].append("NXDOMAIN")
            break
            
        except dns.exception.Timeout:
            logger.warning(f"Timeout querying {record_type}")
            results["errors"].append(f"Timeout on {record_type}")

        except Exception as e:
            logger.error(f"Unexpected DNS error: {e}")
            results["errors"].append(str(e))

    results["metadata"]["finished_at"] = datetime.utcnow().isoformat() + "Z"
    logger.info(f"DNS enumeration finished for {domain}")

    return results
    

