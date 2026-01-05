import requests
import concurrent.futures

# The Source List: Now separated by Protocol
SOURCES = {
    "http": [
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt"
    ],
    "socks4": [
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt"
    ],
    "socks5": [
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt"
    ]
}

def fetch_proxies(protocol):
    proxies = set()
    print(f"💀 Exhuming {protocol} bodies...")
    for url in SOURCES[protocol]:
        try:
            r = requests.get(url, timeout=5)
            for line in r.text.splitlines():
                if ":" in line:
                    proxies.add(line.strip())
        except:
            pass
    return list(proxies)

def check_proxy(proxy_data):
    protocol, proxy = proxy_data
    # The Ritual: We must format the scheme correctly for requests
    try:
        proxies = {
            "http": f"{protocol}://{proxy}",
            "https": f"{protocol}://{proxy}"
        }
        r = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=5)
        if r.status_code == 200:
            return proxy
    except:
        return None

def main():
    total_alive = 0
    readme_stats = []

    # We loop through each protocol (HTTP, SOCKS4, SOCKS5)
    for protocol in SOURCES.keys():
        raw_proxies = fetch_proxies(protocol)
        print(f"⚰️  Found {len(raw_proxies)} raw {protocol} proxies. Testing...")
        
        # Prepare data for the checking function
        check_list = [(protocol, p) for p in raw_proxies]
        alive_proxies = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            results = executor.map(check_proxy, check_list)
            for p in results:
                if p:
                    alive_proxies.append(p)
        
        print(f"🧟 Arised {len(alive_proxies)} {protocol} proxies.")
        total_alive += len(alive_proxies)
        readme_stats.append(f"- **{protocol.upper()}:** {len(alive_proxies)}")

        # Save to separate files (http.txt, socks4.txt, socks5.txt)
        with open(f"{protocol}.txt", "w") as f:
            for p in alive_proxies:
                f.write(p + "\n")

    # Update the README
    with open("README.md", "w") as f:
        f.write(f"# 💀 The Proxy Monarch (Updated Hourly)\n\n")
        f.write(f"![Total Proxies](https://img.shields.io/badge/Total_Online-{total_alive}-brightgreen)\n\n")
        
        f.write(f"## 🛑 STOP USING DEAD PROXIES\n")
        f.write(f"Free proxies die in minutes. For scraping, gaming, or streaming, you need stability.\n\n")
        
        # >>> YOUR AFFILIATE LINK GOES HERE <<<
        f.write(f"### [🚀 CLICK HERE FOR GOD-TIER RESIDENTIAL PROXIES](https://www.smartproxy.org/register/?invitation_code=NRRW4C) <--- \n\n")
        
        f.write(f"## 📊 Current Status\n")
        for stat in readme_stats:
            f.write(f"{stat}\n")
            
        f.write(f"\n## 📥 Download Lists\n")
        f.write(f"- [HTTP List](http.txt)\n")
        f.write(f"- [SOCKS4 List](socks4.txt)\n")
        f.write(f"- [SOCKS5 List](socks5.txt)\n")

if __name__ == "__main__":
    main()
