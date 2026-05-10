import time
import os
import json
import gspread

from flask import Flask
from threading import Thread

from bs4 import BeautifulSoup
from google.oauth2.service_account import Credentials

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# =========================
# FLASK SERVER
# =========================

app = Flask(__name__)

@app.route("/")
def home():
    return "Punishment Bot Running"

def run_web():
    app.run(host="0.0.0.0", port=10000)

web_thread = Thread(target=run_web)
web_thread.daemon = True
web_thread.start()

print("Flask started")

# =========================
# GOOGLE SHEETS
# =========================

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

print("STEP 1")

creds_json = os.environ.get("GOOGLE_CREDENTIALS")

print("STEP 2")

creds_dict = json.loads(creds_json)

print("STEP 3")

creds = Credentials.from_service_account_info(
    creds_dict,
    scopes=scope
)

print("STEP 4")

client = gspread.authorize(creds)

print("STEP 5")

sheet = client.open_by_key(
    "1u8Z6m_KpBGgvyfwFVnc1WfC_ta3Bu-4vurVb9RertGw"
).sheet1

print("Google Sheet connected")

# =========================
# SELENIUM
# =========================

chrome_options = Options()

chrome_options.binary_location = "/usr/bin/chromium"

chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

print("Starting Chrome...")

driver = webdriver.Chrome(options=chrome_options)

print("Chrome started successfully")

URL = "https://bharatmc.net/punishments"

added = set()

print("Starting scraper loop...")

# =========================
# SCRAPER LOOP
# =========================

while True:

    try:

        print("Opening website...")

        driver.get(URL)

        time.sleep(10)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        rows = soup.find_all("tr")

        print(f"Found rows: {len(rows)}")

        for row in rows:

            cols = row.find_all("td")

            if len(cols) < 7:
                continue

            player = cols[0].text.strip()
            ptype = cols[1].text.strip()
            reason = cols[2].text.strip()
            server = cols[3].text.strip()
            issued_by = cols[4].text.strip()
            issued = cols[5].text.strip()
            status = cols[6].text.strip()

            unique = f"{player}-{ptype}-{issued}"

            if unique not in added:

                sheet.append_row([
                    player,
                    ptype,
                    reason,
                    server,
                    issued_by,
                    issued,
                    status
                ])

                added.add(unique)

                print(f"Added {player}")

    except Exception as e:
        print(f"ERROR: {e}")

    time.sleep(300)
