import os
import smtplib
import sys
from email.mime.text import MIMEText

import requests

DATE = "2026-07-03"  # Friday, July 3, 2026
FACILITY_ID = "10857"
API_URL = (
      f"https://phx-api-be-east-1b.kenna.io/v2/tee-times"
      f"?date={DATE}&facilityIds={FACILITY_ID}&returnPromotedRates=true"
)

GMAIL_USER = os.environ["GMAIL_USER"]
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
PHONE_GATEWAY = os.environ["PHONE_GATEWAY"]  # e.g. 2103230455@txt.att.net


def get_tee_times():
      resp = requests.get(API_URL, timeout=20)
      resp.raise_for_status()
      data = resp.json()
      if isinstance(data, list):
                return data
            if isinstance(data, dict):
                      for key in ("teeTimes", "results", "data"):
                                    if key in data and isinstance(data[key], list):
                                                      return data[key]
                                          return []


def send_text(message: str):
      msg = MIMEText(message)
    msg["From"] = GMAIL_USER
    msg["To"] = PHONE_GATEWAY
    msg["Subject"] = ""

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
              server.starttls()
              server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
              server.sendmail(GMAIL_USER, [PHONE_GATEWAY], msg.as_string())


def main():
      tee_times = get_tee_times()
    count = len(tee_times)
    print(f"Checked {DATE}: {count} tee time(s) found.")

    if count > 0:
              times_preview = []
              for slot in tee_times[:5]:
                            t = slot.get("time") or slot.get("teeTime") or slot.get("startTime") or "unknown time"
                            times_preview.append(str(t))
                        msg = f"Tee times OPEN on {DATE} at Starcke Park! {count} slot(s): {', '.join(times_preview)}"
        send_text(msg)
        print("Text sent.")
else:
        print("No tee times available yet.")


if __name__ == "__main__":
      try:
                main()
except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
