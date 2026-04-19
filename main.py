from scanner import XSSScanner

def main():
    print("\n==== MINI XSS VULNERABILITY FINDER ====\n")
    
    target_url = input("Enter Target URL: ").strip()

    # Default payload file 
    payload_file = "payloads.txt"

    if not target_url.startswith("http"):
        target_url = "http://" + target_url

    scanner = XSSScanner(target_url, payload_file)
    scanner.run()

if __name__ == "__main__":
    main()