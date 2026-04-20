# 🛡️ Mini XSS Vulnerability Finder

A simple Python-based tool to detect **Cross-Site Scripting (XSS)** vulnerabilities in web applications by crawling pages and testing input fields with payloads.

---

## 📌 Features

* Crawls web pages within the target domain
* Extracts forms and input fields automatically
* Tests both **GET** and **POST** requests
* Uses multiple XSS payloads for detection
* Displays vulnerabilities in a clean CLI report

---

## 🛠️ Tech Stack

* Python
* Requests
* BeautifulSoup (bs4)

---

## 📂 Project Structure

```
xss_finder/
│
├── scanner.py          # Core scanning logic
├── main.py             # Entry point (runs the scanner)
├── payload_loader.py   # Loads payloads from file
├── payloads.txt        # XSS payload list
```

---

## ⚙️ Installation

1. Clone the repository:

```
git clone <youChange the installation session like 
```bash 
git clone https://github.com/Malu01/xss_finder.git 
cd xss_finder
```

2. Install dependencies:

```
pip install requests beautifulsoup4
```

---

## ▶️ Usage

Run the scanner:

```
python main.py
```

Enter the target URL:

```
Enter Target URL: http://example.com
```

---

## 🧪 How It Works

1. Crawls the given website
2. Finds all forms and inputs
3. Injects XSS payloads
4. Checks if payload is reflected in response
5. Reports potential vulnerabilities

---


