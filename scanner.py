import requests, time, os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


G, R, Y, C, W, RS = '\033[92m', '\033[91m', '\033[93m', '\033[96m', '\033[97m', '\033[0m'
BD = '\033[1m'

class XSSScanner:
    def __init__(self, target_url, payload_file, max_pages=20):
        self.target_url = target_url
        self.visited = set()
        self.vulns = []
        self.max_pages = max_pages
        self.session = requests.Session()
        self.session.headers = {"User-Agent": "WolfScanner/3.0"}
        self.payloads = self.load_payloads(payload_file)

    def load_payloads(self, file_path):
        
        if not os.path.exists(file_path):
            print(f"{R}[!] Error: '{file_path}' not found{RS}")
            return []
        with open(file_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f.readlines() if line.strip()]

    def crawl_and_scan(self, url):
        
        if len(self.visited) >= self.max_pages or url in self.visited:
            return
        
        self.visited.add(url)
        print(f"{C}[*] Scanning: {url}{RS}")

        try:
            res = self.session.get(url, timeout=5)
            soup = BeautifulSoup(res.text, 'html.parser')
            
           
            self.scan_forms(url, soup)

            
            for a in soup.find_all('a', href=True):
                link = urljoin(url, a['href'])
                if urlparse(link).netloc == urlparse(self.target_url).netloc:
                    self.crawl_and_scan(link)
        except:
            pass

    def scan_forms(self, url, soup):
        
        forms = soup.find_all('form')
        for form in forms:
            action = urljoin(url, form.get('action') or "")
            method = form.get('method', 'get').lower()
            inputs = [i.get('name') for i in form.find_all(['input', 'textarea']) if i.get('name')]

            if not inputs: continue

            for p in self.payloads:
                data = {name: p for name in inputs}
                try:
                    if method == 'post':
                        resp = self.session.post(action, data=data, timeout=5)
                    else:
                        resp = self.session.get(action, params=data, timeout=5)

                    if p in resp.text:
                        print(f"  {R}{BD}[!] VULNERABILITY FOUND AT: {url}{RS}")
                        self.vulns.append({"url": url, "payload": p, "method": method.upper()})
                        break
                except:
                    continue

    def print_summary_table(self, duration):
        
        print(f"\n{W}{'━'*75}{RS}")
        print(f"  {BD}{W}FINAL SCAN REPORT{RS}")
        print(f"{W}{'━'*75}{RS}")
        print(f"  {C}Target URL{RS}      : {W}{self.target_url}{RS}")
        print(f"  {C}Pages Scanned{RS}   : {W}{len(self.visited)}{RS}")
        print(f"  {C}Vulnerabilities{RS} : {R if self.vulns else G}{len(self.vulns)}{RS}")
        print(f"  {C}Time Elapsed{RS}    : {W}{duration}s{RS}")
        print(f"{W}{'─'*75}{RS}")

        if self.vulns:
            # Table Header
            print(f"  {R}{BD}{'TARGET URL':<40} | {'METHOD':<8} | {'PAYLOAD'}{RS}")
            print(f"  {W}{'-'*72}{RS}")
            for v in self.vulns:
                # URL  (Clean output)
                display_url = (v['url'][:37] + '..') if len(v['url']) > 37 else v['url']
                print(f"  {W}{display_url:<40} | {v['method']:<8} | {Y}{v['payload']}{RS}")
        else:
            print(f"  {G}✓ No XSS vulnerabilities found. Website seems safe.{RS}")
        
        print(f"{W}{'━'*75}{RS}\n")

    def run(self):
        if not self.payloads:
            return
            
        print(f"\n{C}{BD}      WOLF XSS SCANNER v3.0 - ADVANCED CLI      {RS}")
        print(f"{C}{'='*55}{RS}\n")
        
        start_time = time.time()
        self.crawl_and_scan(self.target_url)
        end_time = time.time()
        
        duration = round(end_time - start_time, 2)
        self.print_summary_table(duration)

if __name__ == "__main__":
    u = input(f"{Y}Enter Target URL: {RS}")
    f = input(f"{Y}Enter Payloads File (e.g., payloads.txt): {RS}")
    
    if not u.startswith("http"): u = "http://" + u
    
    scanner = XSSScanner(u, f)
    scanner.run()
