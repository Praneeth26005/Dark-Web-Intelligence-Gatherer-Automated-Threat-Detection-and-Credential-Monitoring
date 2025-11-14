import os
import smtplib
from email.message import EmailMessage
import requests
from dotenv import load_dotenv
load_dotenv()

SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK")  # optional
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT") or 587)
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
ALERT_FROM = os.getenv("ALERT_FROM", "alerts@example.com")
ALERT_TO = os.getenv("ALERT_TO", "ops@example.com")

def send_slack_alert(text):
    if not SLACK_WEBHOOK:
        print("SLACK_WEBHOOK not configured. Skipping slack alert.")
        return
    payload = {"text": text}
    r = requests.post(SLACK_WEBHOOK, json=payload, timeout=10)
    r.raise_for_status()
    return True

def send_email_alert(subject, body, to_address=ALERT_TO):
    if not SMTP_SERVER or not SMTP_USER or not SMTP_PASS:
        print("SMTP not configured. Skipping email alert.")
        return
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = ALERT_FROM
    msg["To"] = to_address
    msg.set_content(body)
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as s:
        s.starttls()
        s.login(SMTP_USER, SMTP_PASS)
        s.send_message(msg)
    return True
