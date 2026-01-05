import requests
import concurrent.futures

# 1. The Graveyards (Sources of raw proxies)
# We pull from other massive lists to find the few that are alive
SOURCES = [
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt"
]

def fetch_proxies():
    proxies = set()
    print("💀 Exhuming bodies...")
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=5)
            for line in r.text.splitlines():
                if ":" in line:
                    proxies.add(line.strip())
        except:
            pass
    return list(proxies)

def check_proxy(proxy):
    # 2. The Ritual (Testing if the proxy is alive)
    # We try to connect to httpbin.org. If it answers, the proxy is alive.
    try:
        r = requests.get("http://httpbin.org/ip", proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"}, timeout=5)
        if r.status_code == 200:
            return proxy
    except:
        return None

def main():
    raw_proxies = fetch_proxies()
    print(f"⚰️  Found {len(raw_proxies)} raw proxies. Testing...")
    
    alive_proxies = []
    # We use 50 concurrent threads to test them fast
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(check_proxy, raw_proxies)
        for p in results:
            if p:
                alive_proxies.append(p)

    print(f"🧟 Arised {len(alive_proxies)} undead proxies.")

    # 3. The Monument (Saving the list)
    with open("http.txt", "w") as f:
        for p in alive_proxies:
            f.write(p + "\n")
            
    # 4. The Trap (Updating the README with the Affiliate Link)
    with open("README.md", "w") as f:
        f.write(f"# 💀 The Proxy Monarch (Updated Hourly)\n\n")
        f.write(f"![Proxy Status](https://img.shields.io/badge/Proxies_Online-{len(alive_proxies)}-brightgreen)\n\n")
        
        f.write(f"## 🛑 STOP USING DEAD PROXIES\n")
        f.write(f"Free proxies are slow and unreliable. If you need speed for scraping or gaming:\n\n")
        
        # THIS IS WHERE THE MONEY COMES FROM
        f.write(f"### [🚀 CLICK HERE FOR GOD-TIER RESIDENTIAL PROXIES (FAST)](https://www.smartproxy.org/register/?invitation_code=NRRW4C) <--- Recommended\n\n")
        
        f.write(f"## 🆓 Free Public List (Slow but Free)\n")
        f.write(f"Updated automatically every hour.\n\n")
        f.write(f"```\n")
        for p in alive_proxies[:50]: # Show top 50
            f.write(p + "\n")
        f.write(f"...\n```\n")
        f.write(f"### [Download Full List](http.txt)")

if __name__ == "__main__":
    main()
