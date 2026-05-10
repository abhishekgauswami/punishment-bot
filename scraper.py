import time
import gspread

from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json",
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

        data = [col.text.strip() for col in cols[:7]]

        print(data)

        sheet.append_row(data)

    time.sleep(300)