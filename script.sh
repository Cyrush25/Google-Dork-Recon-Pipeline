#!/bin/bash

# =============================
# Google Dork Scanner (Fixed)
# =============================

if [[ $# -lt 3 ]]; then
    echo "Usage: $0 domains.txt -o output.txt"
    exit 1
fi

DOMAIN_FILE="$1"
OUTPUT_FILE="$3"

API_KEY="$SERPAPI_KEY"

if [[ -z "$API_KEY" ]]; then
    echo "Set SERPAPI_KEY first:"
    echo "export SERPAPI_KEY=YOUR_KEY"
    exit 1
fi

TMP_FILE=$(mktemp)

# -----------------------------
# Dorks
# -----------------------------

DORKS=(
'site:*replace* inurl:installer-log.txt intext:DUPLICATOR INSTALL-LOG'
'site:*replace* confidential | top secret | classified | undisclosed'
'site:*replace* intitle:"Index of"'
'site:*replace* filetype:xls'
'site:*replace* "<?php"'
'site:*replace* inurl:redirect'
'site:"*replace*" ext:(doc | pdf | xls | txt | rtf | odt | ppt | xml)'
'site:*replace* intitle:"index of" -inurl:(jsp|pl|php|html|aspx|htm|cf|shtml)'
'site:*replace* intitle:"Index of" | "parent directory"'
'site:*replace* inurl:redir | inurl:url | inurl:redirect | inurl:return'
'site:*replace* ext:(doc | pdf | xls | txt | rtf | odt | ppt | xml | log | dat)'
'site:*replace* ext:xml | ext:conf | ext:cnf | ext:reg | ext:inf | ext:rdp | ext:cfg | ext:txt | ext:ora | ext:ini | ext:log | ext:bkf | ext:bkp | ext:bak | ext:old | ext:backup'
'site:*replace* intext:"sql syntax near" | intext:"Warning: mysql_connect()"'
)

# -----------------------------
# URL Encode (Fixed)
# -----------------------------

urlencode() {
    python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.stdin.read().strip()))"
}

# -----------------------------
# Google Search
# -----------------------------

search_google() {

    QUERY="$1"

    ENCODED=$(echo "$QUERY" | urlencode)

    RESPONSE=$(curl -s \
      "https://serpapi.com/search.json?q=$ENCODED&engine=google&api_key=$API_KEY&num=100")

    # Extract only if exists
    echo "$RESPONSE" | jq -r '.organic_results[]?.link'
}

# -----------------------------
# Main
# -----------------------------

echo "[+] Starting scan..."

while read -r DOMAIN; do

    [[ -z "$DOMAIN" ]] && continue

    echo "[*] Scanning: $DOMAIN"

    for DORK in "${DORKS[@]}"; do

        QUERY="${DORK//\*replace\*/$DOMAIN}"

        echo "    [+] $QUERY"

        RESULTS=$(search_google "$QUERY")

        if [[ -n "$RESULTS" ]]; then
            echo "$RESULTS" >> "$TMP_FILE"
        fi

        sleep 1

    done

done < "$DOMAIN_FILE"

# -----------------------------
# Cleanup
# -----------------------------

sort -u "$TMP_FILE" > "$OUTPUT_FILE"

rm "$TMP_FILE"

echo
echo "[+] Scan complete"
echo "[+] Saved to: $OUTPUT_FILE"
