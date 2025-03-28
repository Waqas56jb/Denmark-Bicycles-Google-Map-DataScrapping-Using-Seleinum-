from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import random
import re
import csv

# Helper function to extract text from an element
def get_element_text(driver, xpath):
    try:
        element = driver.find_element(By.XPATH, xpath)
        return element.text.strip()
    except NoSuchElementException:
        return ""

# Helper function to extract an attribute from an element
def get_element_attribute(driver, xpath, attribute):
    try:
        element = driver.find_element(By.XPATH, xpath)
        return element.get_attribute(attribute)
    except NoSuchElementException:
        return ""

# List of keywords for cycle locations in Denmark (mirroring Playwright’s search approach)
keywords = [
    "Cykelbutik i Danmark", "Bicycle shop Denmark", "Cykelværksted i Danmark", "Bicycle repair Denmark",
    "Cykeludlejning i Danmark", "Bicycle rental Denmark", "Elcykel butik Danmark", "Electric bike shop Denmark",
    "Mountainbike butik Danmark", "Mountain bike shop Denmark", "Racercykel butik Danmark", "Road bike shop Denmark",
    "Cykelhandler Danmark", "Bicycle dealer Denmark", "Cykel specialist Danmark", "Bicycle specialist Denmark",
    "Cykel butik København", "Bicycle shop Copenhagen", "Cykel butik Aarhus", "Bicycle shop Aarhus",
    "Cykel butik Odense", "Bicycle shop Odense", "Cykel butik Aalborg", "Bicycle shop Aalborg"
]

# Maximum listings to scrape per keyword (set to 25 as in Playwright’s main function)
max_listings = 25

# Fields to match Playwright’s extracted data
fieldnames = [
    "Keyword", "Name", "Type", "Plus Code", "Rating", "Address", "Website", "Phone",
    "Reviews Count", "Latitude", "Longitude", "Map URL"
]

# Set up Chrome WebDriver with English language
options = webdriver.ChromeOptions()
options.add_argument('--lang=en-US')
driver = webdriver.Chrome(options=options)

# Initialize list to store all data
data_list = []

# Main scraping loop
for keyword in keywords:
    print(f"Processing keyword: {keyword}")
    try:
        # Navigate to Google Maps
        driver.get("https://www.google.com/maps?hl=en")
        time.sleep(3)

        # Enter search keyword
        search_box = driver.find_element(By.ID, "searchboxinput")
        search_box.clear()
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.ENTER)
        time.sleep(3)

        # Check if results exist
        try:
            feed = driver.find_element(By.XPATH, '//div[@role="feed"]')
        except NoSuchElementException:
            print(f"No results for {keyword}")
            continue

        # Scroll to load listings (mimics Playwright’s scrolling logic)
        while True:
            listings = driver.find_elements(By.XPATH, '//a[contains(@href, "https://www.google.com/maps/place")]')
            current_listings = len(listings)
            if current_listings >= max_listings:
                break

            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", feed)
            time.sleep(2)

            new_listings = len(driver.find_elements(By.XPATH, '//a[contains(@href, "https://www.google.com/maps/place")]'))
            if new_listings == current_listings:
                if driver.find_elements(By.XPATH, '//p[@class="fontBodyMedium "]//span[text()="You\'ve reached the end of the list."]'):
                    print(f"Reached end of list for {keyword}")
                    break
                elif listings:
                    click_index = max(0, current_listings - 3)
                    listings[click_index].click()
                    time.sleep(2)
                else:
                    break

        # Extract listing URLs (up to max_listings)
        listings = driver.find_elements(By.XPATH, '//a[contains(@href, "https://www.google.com/maps/place")]')[:max_listings]
        urls = [listing.get_attribute('href') for listing in listings]
        print(f"Found {len(urls)} listings for {keyword}")

        # Scrape details from each listing
        for url in urls:
            try:
                driver.get(url)
                time.sleep(3)

                # Extract data using XPaths from Playwright code
                name = get_element_text(driver, '//div[@style="padding-bottom: 4px;"]//h1')
                type_ = get_element_text(driver, '//div[@class="LBgpqf"]//button[@class="DkEaL "]')
                plus_code = get_element_text(driver, '//button[contains(@aria-label, "Plus code:")]//div[contains(@class, "Io6YTe") and contains(@class, "fontBodyMedium")]')
                rating = get_element_text(driver, '//div[@style="padding-bottom: 4px;"]//div[contains(@jslog,"mutable:true;")]/span[1]/span[1]')
                address = get_element_text(driver, '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]')
                website = get_element_attribute(driver, '//a[@data-value="Open website"]', 'href')
                phone = get_element_text(driver, '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]')
                review_raw = get_element_text(driver, '//div[@style="padding-bottom: 4px;"]//div[contains(@jslog,"mutable:true;")]/span[2]')
                reviews_count = re.sub(r'[^\d]', '', review_raw) if review_raw else ""

                # Parse coordinates from URL (mimics Playwright’s parse_coordinates)
                match = re.search(r'@([\d.-]+),([\d.-]+)', url)
                latitude = match.group(1) if match else ""
                longitude = match.group(2) if match else ""

                # Store data in a dictionary
                data_dict = {
                    "Keyword": keyword,
                    "Name": name,
                    "Type": type_,
                    "Plus Code": plus_code,
                    "Rating": rating,
                    "Address": address,
                    "Website": website,
                    "Phone": phone,
                    "Reviews Count": reviews_count,
                    "Latitude": latitude,
                    "Longitude": longitude,
                    "Map URL": url
                }
                data_list.append(data_dict)
                print(f"Scraped: {name}")

            except Exception as e:
                print(f"Error scraping {url}: {e}")

            # Return to search results
            driver.back()
            time.sleep(2)

    except Exception as e:
        print(f"Error with keyword {keyword}: {e}")

# Save data to CSV
if data_list:
    with open('cycle_locations_denmark.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data_list)
    print("Data saved to 'cycle_locations_denmark.csv'.")
else:
    print("No data scraped.")

# Close the browser
driver.quit()