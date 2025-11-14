import os
import pandas as pd
from fuzzywuzzy import fuzz
from notifier import send_slack_alert

DATA_DIR = "sample_data"

def scan_file_for_email(filepath, target_email, fuzzy_threshold=90):
    df = pd.read_csv(filepath, dtype=str).fillna("")
    # direct match
    match_rows = df[df['email'].str.lower() == target_email.lower()]
    if not match_rows.empty:
        return match_rows
    # fuzzy match on email localpart or full
    df['score'] = df['email'].apply(lambda x: fuzz.token_set_ratio(x.lower(), target_email.lower()))
    possible = df[df['score'] >= fuzzy_threshold]
    return possible

def main():
    target_email = "your.email@example.com"  # replace
    for fname in os.listdir(DATA_DIR):
        if not fname.endswith(".csv"):
            continue
        path = os.path.join(DATA_DIR, fname)
        results = scan_file_for_email(path, target_email)
        if not results.empty:
            print(f"Matches in {fname}:")
            print(results.head())
            send_slack_alert(f"Local leak match for {target_email} in {fname}: {len(results)} rows found.")
        else:
            print(f"No matches in {fname}.")

if __name__ == "__main__":
    main()
