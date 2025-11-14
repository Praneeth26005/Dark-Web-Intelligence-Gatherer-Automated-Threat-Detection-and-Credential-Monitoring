import os
import requests
from dotenv import load_dotenv
from notifier import send_slack_alert, send_email_alert

load_dotenv()
HIBP_API_KEY = os.getenv("HIBP_API_KEY")
USER_AGENT = "dw-intel-prototype/1.0 (email@example.com)"  # update contact email

HEADERS = {
    "hibp-api-key": HIBP_API_KEY,
    "User-Agent": USER_AGENT
}

def check_account_breaches(email):
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{requests.utils.requote_uri(email)}"
    params = {"truncateResponse": "false"}
    r = requests.get(url, headers=HEADERS, params=params, timeout=15)
    if r.status_code == 200:
        return r.json()  # list of breaches
    elif r.status_code == 404:
        return []  # not found in breaches
    else:
        r.raise_for_status()

def check_pwned_password_range(prefix):
    # If you implement k-anonymity password check, follow HIBP's k-Anonymity SHA1 API:
    # GET https://api.pwnedpasswords.com/range/{first5hash}
    pass

def main():
    # Example usage: emails to monitor
    emails = ["your.email@example.com"]  # replace with own/test emails
    for e in emails:
        try:
            breaches = check_account_breaches(e)
            if breaches:
                print(f"[ALERT] {e} appears in {len(breaches)} breaches.")
                # format a message
                details = "\n".join([f"{b['Title']} ({b['BreachDate']}) - {b.get('Domain','')}" for b in breaches])
                msg = f"Email {e} found in {len(breaches)} breach(es):\n{details}"
                # notify (optionally)
                send_slack_alert(msg)
                # send_email_alert("HIBP Alert", msg, to_address="ops@example.com")
            else:
                print(f"{e} not found in public breaches.")
        except Exception as ex:
            print("Error checking HIBP:", ex)

if __name__ == "__main__":
    main()
