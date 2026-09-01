import requests
import random
import time
import urllib.parse

TARGET_URL = "http://localhost:8080"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15",
]

def send_legitimate():
    paths = ["/", "/index.html", "/about", "/contact", "/products"]
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    url = f"{TARGET_URL}{random.choice(paths)}"
    try:
        requests.get(url, headers=headers, timeout=3)
        print(f"[OK] Legitimate GET: {url}")
    except requests.exceptions.RequestException:
        pass

def send_brute_force():
    paths = ["/login", "/admin", "/administrator"]
    headers = {"User-Agent": "Hydra/9.0 (Attacker Tool)"}
    target_path = random.choice(paths)
    print(f"[!] Starting Brute-force on {target_path}")
    # Генеруємо 18 запитів поспіль (щоб викликати Alert "понад 15 за хвилину")
    for _ in range(18):
        url = f"{TARGET_URL}{target_path}"
        try:
            requests.post(url, headers=headers, data={"username": "admin", "password": "password123"}, timeout=3)
        except requests.exceptions.RequestException:
            pass
        time.sleep(0.1)

def send_sqli():
    payloads = ["1' OR '1'='1", "admin' --", "' UNION SELECT username, password FROM users--"]
    headers = {"User-Agent": "sqlmap/1.6.8#dev (http://sqlmap.org)"}
    # Кодуємо пейлоад для URL
    safe_payload = urllib.parse.quote(random.choice(payloads))
    url = f"{TARGET_URL}/?id={safe_payload}"
    try:
        requests.get(url, headers=headers, timeout=3)
        print(f"[!] SQL Injection: {url}")
    except requests.exceptions.RequestException:
        pass

def send_path_traversal():
    payloads = ["../../../../etc/passwd", "../../../../windows/win.ini", "%2e%2e%2f%2e%2e%2fetc%2fpasswd"]
    headers = {"User-Agent": "Nikto/2.1.6"}
    url = f"{TARGET_URL}/?file={random.choice(payloads)}"
    try:
        requests.get(url, headers=headers, timeout=3)
        print(f"[!] Path Traversal: {url}")
    except requests.exceptions.RequestException:
        pass

if __name__ == "__main__":
    print(f"Starting Attack Simulation against {TARGET_URL}...\nPress Ctrl+C to stop.")
    while True:
        # Ваги: 70% легітимний трафік, по 10% на атаки
        action = random.choices(
            [send_legitimate, send_brute_force, send_sqli, send_path_traversal],
            weights=[70, 10, 10, 10],
            k=1
        )[0]

        action()
        # Пауза між діями від 0.5 до 2 секунд
        time.sleep(random.uniform(0.5, 2.0))