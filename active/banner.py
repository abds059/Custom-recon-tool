import socket


def run_banner_grab(target, ports, logger=None):
    banners = {}

    if logger:
        logger.info("Starting banner grabbing")

    for port in ports:
        try:
            sock = socket.socket()
            sock.settimeout(2)
            sock.connect((target, port))
            sock.sendall(b"\r\n")
            banner = sock.recv(1024).decode(errors="ignore").strip()
            sock.close()

            if banner:
                banners[port] = banner
                if logger:
                    logger.debug(f"Banner from port {port}: {banner}")
        except Exception:
            continue

    if logger:
        logger.info("Banner grabbing completed")

    return banners
