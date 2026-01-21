import subprocess

def identify_tech(domain, logger=None):
    try:
        result = subprocess.run(
            ["whatweb", domain],
            capture_output=True,
            text=True,
            timeout=20
        )
    except Exception as e:
        if logger:
            logger.error(f"WhatWeb failed: {e}")
        return ""

    if logger:
        logger.info("Technology identification completed")

    return result.stdout.strip()
