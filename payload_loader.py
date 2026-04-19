import os

def load_payloads(file_path):
    if not os.path.exists(file_path):
        print(f"[!] File not found: {file_path}")
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        payloads = [line.strip() for line in f.readlines() if line.strip()]

    return payloads