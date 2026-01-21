def dispatch(args, logger):

    results = {
        "domain": args.domain,
        "passive": {},
        "active": {}
    }

    scan_result = {} 

    if args.dns:
        logger.info("Running DNS enumeration")
        from passive.dns import run_dns_enum
        results["passive"]["dns"] = run_dns_enum(args.domain, logger)

    if args.subdomains:
        logger.info("Running subdomain enumeration")
        from passive.subdomain import run_subdomain_enum
        results["passive"]["subdomains"] = run_subdomain_enum(args.domain, logger)

    if args.whois:
        logger.info("Running WHOIS lookup")
        from passive.whois_lookup import run_whois_lookup
        results["passive"]["whois"] = run_whois_lookup(args.domain, logger)

    if args.portscan:
        logger.info("Running socket-based port scan")
        from active.port_scan import run_port_scan
        scan_result = run_port_scan(args.domain, logger)
        results["active"]["portscan"] = scan_result

        # Banner grabbing only if ports found
        from active.banner import run_banner_grab
        banners = run_banner_grab(
            args.domain,
            scan_result.get("open_ports", []),
            logger
        )
        results["active"]["banners"] = banners

    return results
