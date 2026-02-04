# 🔍 Google Dork Recon Pipeline

An automated OSINT & security reconnaissance framework that transforms Google dork results into actionable security intelligence.

This project chains together:

> **Google Dorking → Crawling → Leak Detection → CVE Scanning → Reporting**

Designed for penetration testers, bug bounty hunters, red teamers, and security researchers.

---

## 📌 Features

* ✅ Automated Google Dork scanning (API-based)
* ✅ Domain-based dork generation
* ✅ URL harvesting and de-duplication
* ✅ Intelligent web crawler
* ✅ Sensitive file discovery
* ✅ Credential & token leak detection
* ✅ Misconfiguration detection
* ✅ CVE scanning (via Nuclei)
* ✅ JSON + TXT reporting
* ✅ Clean CLI interface

---

## 🗂️ Project Structure

```text
google-dork-recon/
│
├── script.sh        # Google dork scanner
├── crawler.py       # Vulnerability crawler
├── seed-domains.txt # Target domains
├── results.txt      # Dork output URLs
├── report.json      # Machine-readable report
├── report.txt       # Human-readable report
└── README.md        # Documentation
```

---

## ⚙️ Requirements

### System

* Linux (Kali recommended)
* Python 3.8+
* Bash

### Packages

```bash
sudo apt update
sudo apt install curl jq python3 python3-pip nuclei -y
```

### Python Libraries

```bash
pip3 install httpx beautifulsoup4 rich tldextract
```

### Nuclei Templates

```bash
nuclei -update-templates
```

---

## 🔑 API Setup (SerpAPI)

This project uses SerpAPI for Google searches (to avoid blocking and TOS violations).

1. Create account: [https://serpapi.com](https://serpapi.com)
2. Get API key
3. Export key:

```bash
export SERPAPI_KEY="YOUR_API_KEY"
```

Verify:

```bash
echo $SERPAPI_KEY
```

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/google-dork-recon.git
cd google-dork-recon
```

Make scripts executable:

```bash
chmod +x script.sh crawler.py
```

---

## 📝 Usage

### 1️⃣ Prepare Targets

Edit `seed-domains.txt`:

```text
example.com
target.org
testsite.net
```

---

### 2️⃣ Run Google Dork Scanner

```bash
./script.sh seed-domains.txt -o results.txt
```

This will:

* Apply multiple dorks
* Query Google
* Extract URLs
* Sort and deduplicate

Output:

```
results.txt
```

---

### 3️⃣ Run Crawler & Vulnerability Scanner

```bash
./crawler.py results.txt
```

This will:

* Crawl each URL
* Detect leaks
* Check sensitive files
* Run Nuclei CVE scans
* Generate reports

Outputs:

```
report.json
report.txt
```

---

## 📄 Report Format

### JSON Report (report.json)

```json
[
  {
    "type": "AWS Key",
    "url": "https://example.com/config.js",
    "evidence": "AKIA..."
  }
]
```

### TXT Report (report.txt)

```text
Type     : Sensitive File
URL      : https://example.com/.env
Evidence : DB_PASSWORD
----------------------------
```

---

## 🔎 Detection Capabilities

### 🔐 Leak Detection

* AWS Keys
* Google API Keys
* JWT Tokens
* Passwords
* Database URLs
* Private Keys
* Environment Variables

### 📂 Sensitive Files

* `.env`
* `.git/config`
* `backup.sql`
* `wp-config.php`
* `settings.py`
* `id_rsa`
* `error.log`

### ⚠️ Misconfigurations

* Open directories
* Debug pages
* Error disclosures
* Config exposures

### 🛡️ CVE Detection

* Uses Nuclei templates
* Medium / High / Critical
* Auto-updatable

---

## 🔄 Workflow Pipeline

```text
Domains
   ↓
Dorks
   ↓
Google Search
   ↓
URLs
   ↓
Crawler
   ↓
Leak Scanner
   ↓
Nuclei CVE
   ↓
Reports
```

---

## 🧩 Customization

### Add New Dorks

Edit `script.sh`:

```bash
DORKS=(
  'site:*replace* new_dork_here'
)
```

---

### Add New Leak Patterns

Edit `crawler.py`:

```python
LEAK_PATTERNS = {
    "New Token": r"TOKEN_[A-Z0-9]+"
}
```

---

### Change Crawl Depth

Edit in `crawler.py`:

```python
MAX_DEPTH = 3
```

---

## ⚡ Performance Tips

* Use VPN / proxy when scanning large targets
* Respect API rate limits
* Increase delays if blocked
* Run Nuclei separately for scale

---

## 🔐 Legal Disclaimer

This project is intended for **educational and authorized security testing only**.

You must have explicit permission before scanning any system you do not own.

The author assumes no responsibility for misuse.

---

## 📈 Roadmap

Planned features:

* [ ] Async multi-thread crawler
* [ ] Proxy rotation
* [ ] Screenshot module
* [ ] Web dashboard
* [ ] CVSS scoring
* [ ] Elastic/Splunk export
* [ ] Burp/ZAP integration

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repo
2. Create branch
3. Commit changes
4. Open PR

---

## ⭐ Credits

* SerpAPI
* ProjectDiscovery Nuclei
* BeautifulSoup
* Rich
* Kali Linux

---

## 📬 Contact

For research collaboration or issues:

Create a GitHub issue or pull request.

---

## 🏁 License

MIT License

---

> Happy Hunting 🚀
