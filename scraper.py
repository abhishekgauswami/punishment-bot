import time
import os
import json
import gspread

from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# LOAD GOOGLE CREDS FROM RENDER ENV
creds_json = os.environ.get("GOOGLE_CREDENTIALS")

print("Loading Google credentials...")

creds_dict = json.loads(creds_json)

creds = ServiceAccountCredentials.from_json_keyfile_dict(
    creds_dict,
    scope
)

client = gspread.authorize(creds)

sheet = client.open_by_key(
    "1u8Z6m_KpBGgvyfwFVnc1WfC_ta3Bu-4vurVb9RertGw"
).sheet1

chrome_options = Options()

chrome_options.binary_location = "/usr/bin/chromium"

chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

URL = "https://bharatmc.net/punishments"

added = set()

while True:

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

    time.sleep(300)
