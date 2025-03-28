#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Google Maps Location Detail Scraper

This script loops through an extended list of keywords (covering many Danish and English variations
for “cykel”, “cykler”, “bike shop”, etc.), opens Google Maps for each keyword, and extracts the following fields:
  - Shop Name
  - Rating (e.g., "5.0")
  - Reviews Count (e.g., "79")
  - Category (e.g., "Bicycle Shop")
  - Address (with postal code)
  - Open/Close Time (e.g., "Open ⋅ Closes 6 PM")
  - Website (e.g., "kgshavecykler.dk")
  - Phone Number (with country code, e.g., "+45 35 42 33 11")
  - Plus Code (e.g., "MHXG+CC")
  - Map URL and location coordinates (Latitude/Longitude extracted from URL)
  
All results are saved in a CSV file.
"""

import csv
import re
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ---------------------------
# EXTENDED KEYWORD LIST
# ---------------------------
KEYWORDS = [
    # Danish & English full phrases and common keywords
    "Cykelbutik i Danmark", "Bicycle shop Denmark",
    "Cykelværksted i Danmark", "Bicycle repair Denmark",
    "Bike shop Denmark", "Cykelforhandler i Danmark", "Bicycle dealer Denmark",
    "Cykelservice i Danmark", "Bicycle service Denmark", "Cykelreparation i Danmark",
    "Bicycle repair shop Denmark", "Brugte cykler i Danmark", "Used bicycles Denmark",
    "Cykeludlejning i Danmark", "Bicycle rental Denmark", "Elcykel butik Danmark",
    "Electric bike shop Denmark", "Cykel butik nær mig", "Bicycle shop near me Denmark",
    "Bike mechanic Denmark", "Cykel mekaniker i Danmark", "Cykel dele butik Danmark",
    "Bicycle parts shop Denmark", "Cykel center Danmark", "Bike center Denmark",
    "Cykelshop Danmark", "Bike workshop Denmark", "Bike service near me Denmark",
    "Cykel værksted nær mig", "Bicycle repair near me Denmark", "Mountainbike butik Danmark",
    "Mountain bike shop Denmark", "Racercykel butik Danmark", "Road bike shop Denmark",
    "Cykelhandler Danmark", "Bicycle retailer Denmark", "Cykel specialist Danmark",
    "Bicycle specialist Denmark", "Cykel butik København", "Bicycle shop Copenhagen",
    "Cykel butik Aarhus", "Bicycle shop Aarhus", "Cykel butik Odense", "Bicycle shop Odense",
    "Cykel butik Aalborg", "Bicycle shop Aalborg", "Cykel butik Esbjerg", "Bicycle shop Esbjerg",
    "Cykel butik Randers", "Bicycle shop Randers", "Cykel butik nær København",
    "Bicycle shop near Copenhagen", "Bedste cykelbutik i Danmark", "Best bicycle shop Denmark",
    "Cykelreparation nær mig", "Bicycle repair near me", "Billige cykler i Danmark",
    "Cheap bicycles Denmark", "Cykel forretning Danmark", "Bike store Denmark",
    # Additional variations (short and colloquial forms)
    "cykel", "cykler", "cykle", "cykelhandel", "cykelværksted", "cykeludlejning",
    "cykelforretning", "cykelmekaniker", "cykelreparation", "cykelservice", "cykelcenter",
    "cykelbutik", "cykel shop", "cykel forhandler", "cykel specialist",
    # English short forms
    "cycle", "cycles", "bike", "bikes", "cycle shop", "bike shop", "bicycle shop",
    "bicycle repair", "bike repair", "cycle repair"
]

# ---------------------------
# SELENIUM SETUP
# ---------------------------
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=chrome_options)

# ---------------------------
# CSV OUTPUT SETUP
# ---------------------------
OUTPUT_FILE = "maps_location_data.csv"
CSV_HEADER = [
    "Keyword", "Shop Name", "Rating", "Reviews Count", "Category", "Address", 
    "Open/Close Time", "Website", "Phone", "Plus Code", "Latitude", "Longitude", "Map URL"
]
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(CSV_HEADER)

# ---------------------------
# HELPER FUNCTIONS
# ---------------------------
def random_sleep(a=2, b=5):
    time.sleep(random.uniform(a, b))

def safe_extract(xpath, method="text"):
    """Extracts text or attribute from a given XPath; returns empty string if not found."""
    try:
        element = WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.XPATH, xpath)))
        if method == "text":
            return element.text.strip()
        elif method.startswith("attr:"):
            attr = method.split(":", 1)[1]
            return element.get_attribute(attr)
    except Exception:
        return ""

def extract_from_url(url, param):
    """Extract latitude/longitude from URL if present."""
    match = re.search(r"@([-0-9\.]+),([-0-9\.]+)", url)
    if match:
        return match.group(1) if param == "lat" else match.group(2)
    return ""

def extract_reviews_count(text):
    """Extracts numeric value inside parentheses e.g. (166) -> 166."""
    m = re.search(r"\((\d+)\)", text)
    return m.group(1) if m else ""

def save_row(row):
    with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)

# ---------------------------
# MAIN SCRAPER LOGIC
# ---------------------------
for keyword in KEYWORDS:
    try:
        driver.get("https://www.google.com/maps")
        random_sleep(3, 5)

        # Locate the search box, input the keyword, and submit
        search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "searchboxinput")))
        search_box.clear()
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.ENTER)
        random_sleep(5, 7)

        # Scroll down to load results (adjust scroll count if necessary)
        for _ in range(20):
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            random_sleep(2, 4)

        # Attempt to locate shop cards in the sidebar
        shops = driver.find_elements(By.XPATH, '//div[@role="article"]')
        print(f"[{keyword}] Found {len(shops)} shop cards")

        if len(shops) == 0:
            # No shop cards found; fallback to extracting main location details
            print(f"[{keyword}] No shop cards found. Extracting main location details.")
            shop_name = safe_extract('//h1[contains(@class,"fontHeadlineLarge")]')
            address = safe_extract('//button[@data-item-id="address"]')
            plus_code = safe_extract('//button[@data-item-id="oloc"]')
            map_url = driver.current_url
            latitude = extract_from_url(map_url, "lat")
            longitude = extract_from_url(map_url, "lng")
            # For fallback, leave other fields empty
            empty = ""
            row = [
                keyword, shop_name, empty, empty, empty, address,
                empty, empty, empty, plus_code, latitude, longitude, map_url
            ]
            save_row(row)
        else:
            # Iterate over each shop card found and extract details
            for shop in shops:
                try:
                    driver.execute_script("arguments[0].click();", shop)
                    random_sleep(4, 6)

                    shop_name = safe_extract('//h1[contains(@class,"fontHeadlineLarge")]')
                    rating = safe_extract('//span[contains(@class,"MW4etd")]')
                    reviews_raw = safe_extract('//button[contains(@aria-label,"reviews")]')
                    reviews_count = extract_reviews_count(reviews_raw)
                    category = safe_extract('//button[contains(@aria-label,"Category")]')
                    address = safe_extract('//button[@data-item-id="address"]')
                    open_close = safe_extract('//span[contains(text(),"Open") and contains(text(),"Closes")]')
                    website = safe_extract('//a[@data-item-id="authority"]', method="attr:href")
                    phone = safe_extract('//button[@data-item-id="phone"]')
                    plus_code = safe_extract('//button[@data-item-id="oloc"]')
                    map_url = driver.current_url
                    latitude = extract_from_url(map_url, "lat")
                    longitude = extract_from_url(map_url, "lng")

                    row = [
                        keyword, shop_name, rating, reviews_count, category, address,
                        open_close, website, phone, plus_code, latitude, longitude, map_url
                    ]
                    save_row(row)
                    print(f"✅ Saved: {shop_name if shop_name else 'Unnamed Shop'}")
                    driver.execute_script("window.history.go(-1)")
                    random_sleep(4, 6)
                except Exception as inner_e:
                    print(f"❌ Error processing a shop under keyword [{keyword}]: {inner_e}")
                    continue
    except Exception as e:
        print(f"❌ Error processing keyword [{keyword}]: {e}")
        continue

print("✅ Scraping Completed.")
driver.quit()
