import os, smtplib
from email.mime.text import MIMEText
import requests

DATE = "2026-07-03"
FACILITY_ID = "10857"
ALIAS = "starcke-park"
API_URL = f"https://phx-api-be-east-1b.kenna.io/v2/tee-times?date={DATE}&facilityIds={FACILITY_ID}&returnPromotedRates=true"
BOOKING_LINK = f"https://starcke-park.book.teeitup.com/?course={FACILITY_ID}&date={DATE}"
GMAIL_USER = os.environ["GMAIL_USER"]
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
PHONE_GATEWAY = os.environ["PHONE_GATEWAY"]
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36", "Referer": "https://starcke-park.book.teeitup.com/", "Origin": "https://starcke-park.book.teeitup.com", "Accept": "application/json", "x-be-alias": ALIAS}
TEST_MODE = False

resp = requests.get(API_URL, headers=HEADERS, timeout=20)
print(f"HTTP status: {resp.status_code}")
data = resp.json() if resp.status_code == 200 else []
day_block = data[0] if isinstance(data, list) and len(data) > 0 else {}
tee_times = day_block.get("teetimes", [])
tee_times = [{"time": "2026-07-03T08:10:00"}, {"time": "2026-07-03T08:20:00"}] if TEST_MODE else tee_times
count = len(tee_times)
times_preview = ", ".join(str(t.get("time") or t.get("teeTime") or t.get("startTime") or "unknown")[11:16] for t in tee_times[:5])
message = f"Tee time(s) OPEN at Starcke Park on {DATE}! Times: {times_preview}. Book now: {BOOKING_LINK}"
print(f"Checked {DATE}: {count} tee time(s) found.")

msg = MIMEText(message)
_set1 = msg.__setitem__("From", GMAIL_USER)
_set2 = msg.__setitem__("To", PHONE_GATEWAY)
_set3 = msg.__setitem__("Subject", "")
server = smtplib.SMTP("smtp.gmail.com", 587) if count > 0 else None
_a = server and server.starttls()
_b = server and server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
_c = server and server.sendmail(GMAIL_USER, [PHONE_GATEWAY], msg.as_string())
_d = server and server.quit()
print("Text sent." if count > 0 else "No tee times available yet.")
