#!/usr/bin/env python3

import httpx
import re
import json
import subprocess
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from rich.console import Console
from rich.table import Table
import tldextract

console = Console()

# =====================
# Config
# =====================

MAX_DEPTH = 2
TIMEOUT = 10
NUCLEI = True

HEADERS = {
    "User-Agent": "LeakScanner/1.0"
}

# =====================
# Leak Patterns
# =====================

LEAK_PATTERNS = {

    "AWS Key": r"AKIA[0-9A-Z]{16}",
    "Google API": r"AIza[0-9A-Za-z_-]{35}",
    "JWT": r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+",
    "Password": r"password\s*=\s*[\"'].*?[\"']",
    "DB String": r"(mysql|postgres|mongodb)://",
    "Private Key": r"-----BEGIN PRIVATE KEY-----",
    ".env File": r"DB_PASSWORD|SECRET_KEY|API_KEY",
    "Git Config": r"\.git/config",
}

# =====================
# Sensitive Files
# =====================

SENSITIVE_PATHS = [

    ".env",
    ".git/config",
    "backup.sql",
    "db.sql",
    "dump.sql",
    "config.php",
    "wp-config.php",
    "settings.py",
    "web.config",
    "id_rsa",
    ".htpasswd",
    "error.log"
]

# =====================
# Globals
# =====================

visited = set()
findings = []


# =====================
# Helpers
# =====================

def normalize(url):
    if not url.startswith("http"):
        return "http://" + url
    return url


def same_domain(u1, u2):
    d1 = tldextract.extract(u1).registered_domain
    d2 = tldextract.extract(u2).registered_domain
    return d1 == d2


# =====================
# Leak Scanner
# =====================

def scan_content(url, text):

    for name, pattern in LEAK_PATTERNS.items():

        if re.search(pattern, text, re.I):
            findings.append({
                "type": name,
                "url": url,
                "evidence": pattern
            })


# =====================
# Sensitive Files
# =====================

def check_sensitive(base):

    for path in SENSITIVE_PATHS:

        url = urljoin(base, path)

        try:
            r = client.get(url)

            if r.status_code == 200 and len(r.text) > 50:

                findings.append({
                    "type": "Sensitive File",
                    "url": url,
                    "evidence": path
                })

        except:
            pass


# =====================
# Crawl
# =====================

def crawl(url, depth=0):

    if depth > MAX_DEPTH:
        return

    if url in visited:
        return

    visited.add(url)

    try:
        r = client.get(url)

        if r.status_code != 200:
            return

        text = r.text

        scan_content(url, text)

        soup = BeautifulSoup(text, "html.parser")

        for a in soup.find_all("a", href=True):

            link = urljoin(url, a["href"])
            link = link.split("#")[0]

            if link.startswith("http") and same_domain(url, link):
                crawl(link, depth + 1)

    except:
        pass


# =====================
# Nuclei Runner
# =====================

def run_nuclei(target):

    try:

        result = subprocess.check_output(
            ["nuclei", "-u", target, "-severity", "medium,high,critical"],
            stderr=subprocess.DEVNULL
        ).decode()

        return result.strip()

    except:
        return ""


# =====================
# Main
# =====================

if len(sys.argv) != 2:

    print(f"Usage: {sys.argv[0]} urls.txt")
    sys.exit(1)


URL_FILE = sys.argv[1]

with open(URL_FILE) as f:
    targets = [normalize(x.strip()) for x in f if x.strip()]


client = httpx.Client(
    headers=HEADERS,
    timeout=TIMEOUT,
    follow_redirects=True,
    verify=False
)


console.print("[bold green][+] Starting Leak Scanner[/]\n")

for url in targets:

    console.print(f"[cyan][*] Scanning {url}[/]")

    check_sensitive(url)
    crawl(url)

    if NUCLEI:
        out = run_nuclei(url)

        if out:
            findings.append({
                "type": "Nuclei CVE",
                "url": url,
                "evidence": out
            })


client.close()


# =====================
# Report
# =====================

json_report = "report.json"
txt_report = "report.txt"

with open(json_report, "w") as f:
    json.dump(findings, f, indent=2)


with open(txt_report, "w") as f:

    for item in findings:

        f.write(f"""
Type     : {item['type']}
URL      : {item['url']}
Evidence : {item['evidence']}
----------------------------
""")


# =====================
# Pretty Output
# =====================

table = Table(title="LeakScan Report")

table.add_column("Type")
table.add_column("URL")
table.add_column("Evidence")

for i in findings:
    table.add_row(i["type"], i["url"], i["evidence"])

console.print(table)

console.print(f"\n[bold green][+] Saved: {json_report}, {txt_report}")
