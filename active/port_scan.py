import socket


COMMON_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 139, 143,
    443, 445, 3306, 3389, 8080
]


def run_port_scan(target, logger=None, timeout=1):
    open_ports = []

    if logger:
        logger.info(f"Starting socket-based port scan on {target}")

    for port in COMMON_PORTS:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((target, port))
            sock.close()

            if result == 0:
                open_ports.append(port)
                if logger:
                    logger.debug(f"Port {port} is open")
        except Exception:
            continue

    if logger:
        logger.info(f"Port scan completed, {len(open_ports)} open ports found")

    return {
        "target": target,
        "open_ports": open_ports
    }
