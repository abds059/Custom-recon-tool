import socket
import ssl

def identify_tech(domain, port=80, use_ssl=False, logger=None):
    
    try:
        sock = socket.create_connection((domain, port), timeout=10)
        
        if use_ssl:
            context = ssl.create_default_context()
            sock = context.wrap_socket(sock, server_hostname=domain)
        
        # Send a basic HTTP GET request
        request = f"GET / HTTP/1.1\r\nHost: {domain}\r\nConnection: close\r\n\r\n"
        sock.sendall(request.encode())
        
        response = b""
        while True:
            data = sock.recv(4096)
            if not data:
                break
            response += data
        
        sock.close()
        response_text = response.decode(errors="ignore")
        
        # Basic technology fingerprinting from headers and HTML
        tech = []
        headers, _, body = response_text.partition("\r\n\r\n")
        
        if "Server:" in headers:
            server_line = [line for line in headers.split("\r\n") if line.startswith("Server:")][0]
            tech.append(server_line)
        
        if "X-Powered-By:" in headers:
            xp_line = [line for line in headers.split("\r\n") if line.startswith("X-Powered-By:")][0]
            tech.append(xp_line)
        
        # Simple HTML checks
        if "<meta name=\"generator\"" in body:
            start = body.find("<meta name=\"generator\"")
            end = body.find(">", start)
            meta_tag = body[start:end+1]
            tech.append(meta_tag)
        
        if logger:
            logger.info("Technology identification completed via socket")
        
        return "\n".join(tech) if tech else "No tech info found"
    
    except Exception as e:
        if logger:
            logger.error(f"Socket-based tech identification failed: {e}")
        return ""
