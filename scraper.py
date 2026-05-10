import time
import csv

from flask import Flask, send_file
from threading import Thread

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# =========================
# FLASK SERVER
# =========================

app = Flask(__name__)

@app.route("/")
def home():
    return send_file("punishments.csv", as_attachment=True)

def run_web():
    app.run(host="0.0.0.0", port=10000)

web_thread = Thread(target=run_web)
web_thread.daemon = True
web_thread.start()

print("Flask started")

# =========================
# CSV FILE
# =========================

csv_file = "punishments.csv"

try:
    with open(csv_file, "x", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Player",
            "Type",
            "Reason",
            "Server",
            "Issued By",
            "Issued",
            "Status"
        ])
except:
    pass

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

                with open(csv_file, "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)

                    writer.writerow([
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
