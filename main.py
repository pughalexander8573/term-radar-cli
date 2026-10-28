#!/usr/bin/env python3
import requests, re, sys
from datetime import date

# Fetch trending repositories from GitHub API (using search for recent AI repos)
url = "https://api.github.com/search/repositories?q=topic:ai+created:>" + \
      str(date.today().replace(day=1)) + "&sort=stars&order=desc&per_page=20"
headers = {"Accept": "application/vnd.github.v3+json"}
try:
    resp = requests.get(url, headers=headers, timeout=10)
    repos = resp.json().get("items", [])
except Exception as e:
    print(f"Error fetching data: {e}", file=sys.stderr)
    sys.exit(1)

# Extract potential new terms: repo names and topics
terms = set()
for repo in repos:
    # Split repo name into words
    words = re.split(r'[-_\s]', repo.get("name", ""))
    for w in words:
        if w and w.isalpha() and len(w) > 2 and not w.lower() in {"the", "and", "for"}:
            terms.add(w.lower())
    # Add topics
    for t in repo.get("topics", []):
        if len(t) > 2 and t.isalpha():
            terms.add(t.lower())

# Print radar list sorted alphabetically
print(f"# AI Term Radar - {date.today().isoformat()}")
for term in sorted(terms):
    print(f"- {term}")