import time
import urllib.request
from datetime import datetime

def check_site(url):
    if not url.startswith("http"):
        url = "https://" + url
    start = time.time()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        urllib.request.urlopen(req, timeout=5)
        ms = int((time.time() - start) * 1000)
        return "ONLINE", ms
    except Exception:
        return "OFFLINE", 0

print("Monitor v3 ALERT MODE - quiet when all good, alerts when DOWN")

while True:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("sites.txt") as f:
        sites = [s.strip() for s in f.read().splitlines() if s.strip()]

    online = 0
    down_sites = []
    for site in sites:
        status, ms = check_site(site)
        emoji = "✅" if status == "ONLINE" else "❌"
        if status == "ONLINE":
            online += 1
        else:
            down_sites.append(site)
        line = f"{now} - {site} - {emoji} {status} ({ms}ms)"
        print(line)
        with open("results.txt", "a") as out:
            out.write(line + "\n")

    if down_sites:
        print("\n🚨🚨 ALERT! DOWN: " + ", ".join(down_sites) + " 🚨🚨")
        print("\a")  # beep
        with open("alerts.txt", "a") as a:
            a.write(f"{now} - DOWN: {', '.join(down_sites)}\n")
    else:
        print(f"--- All good: {online}/{len(sites)} ONLINE ---")

    print("--- waiting 10s ---\n")
    time.sleep(10)
