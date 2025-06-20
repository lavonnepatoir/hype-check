import time
import random
import os
import pandas as pd
import undetected_chromedriver as uc
from datetime import datetime, timedelta
from urllib.parse import quote_plus

# === File Paths ===
CSV_PATH = "movie_metadata.csv"
SAVE_DIR = r"C:\Users\bookw\OneDrive\Documents\Summer 2025\hype-check"
BASE_URL = "https://trends.google.com/trends/explore?date={date_range}&geo=US&q={query}&hl=en"

# === Read Metadata ===
metadata = pd.read_csv(CSV_PATH)
done_files = set(os.listdir(SAVE_DIR))

for _, row in metadata.iterrows():
    title = row["Title"]
    release_date = pd.to_datetime(row["Release Date"])
    filename = f"trends_{title.replace(' ', '_')}.csv"

    if filename in done_files:
        print(f"✅ Already processed: {filename}")
        continue

    start = (release_date - timedelta(days=60)).strftime("%Y-%m-%d")
    end = (release_date + timedelta(days=14)).strftime("%Y-%m-%d")
    date_range = f"{start} {end}"
    query = quote_plus(title)
    url = BASE_URL.format(date_range=date_range, query=query)

    print(f"🌐 Opening: {title}")
    options = uc.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--window-size=1200,800")

    driver = uc.Chrome(options=options)
    driver.get(url)

    wait_time = random.randint(20, 30)
    print(f"⏳ Please manually export as CSV and save as: {filename}")
    print(f"📥 Waiting {wait_time} seconds...")
    time.sleep(wait_time)

    driver.quit()

    pause = random.randint(10, 25)
    print(f"😴 Cooling down for {pause} seconds...\n")
    time.sleep(pause)

print("✅ All movies processed!")
