import os
import requests
from dotenv import load_dotenv
from notifier import send_slack_alert

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}

def search_github_code(query, per_page=30):
    url = "https://api.github.com/search/code"
    params = {"q": query, "per_page": per_page}
    r = requests.get(url, headers=HEADERS, params=params, timeout=15)
    r.raise_for_status()
    return r.json()

def build_secret_queries():
    # Simple examples: look for AWS access key-like patterns, 'AKIA' prefix, or 'BEGIN RSA PRIVATE KEY'
    queries = [
        'AKIA in:file language:python',
        '"BEGIN RSA PRIVATE KEY" in:file',
        'password in:file extension:env',
        'api_key in:file'
    ]
    return queries

def main():
    for q in build_secret_queries():
        try:
            res = search_github_code(q)
            total = res.get('total_count',0)
            if total > 0:
                msg = f"GitHub code search: query `{q}` returned {total} hits (first page)."
                print(msg)
                send_slack_alert(msg)
            else:
                print(f"No hits for query `{q}`")
        except Exception as e:
            print("GitHub search error:", e)

if __name__ == "__main__":
    main()
