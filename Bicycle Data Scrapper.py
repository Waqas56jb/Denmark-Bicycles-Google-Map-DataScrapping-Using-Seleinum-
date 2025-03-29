import csv
import time
import random
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# ---------------------------
# LOCATIONS LIST (Keywords with Locations)
# ---------------------------
base_keywords = [
    "Cykelbutik i Danmark", "Bicycle shop Denmark", "Cykelværksted i Danmark", "Bicycle repair Denmark",
    "Cykeludlejning i Danmark", "Bicycle rental Denmark", "Elcykel butik Danmark", "Electric bike shop Denmark",
    "Cykelforretning i Danmark", "Bicycle store Denmark", "Cykelmekaniker i Danmark", "Bike mechanic Denmark",
    "Cykelcenter i Danmark", "Cycle center Denmark", "Cykelhandel i Danmark", "Bicycle retail Denmark",
    "Cykel butik København", "Bicycle shop Copenhagen", "Cykelbutik København", "Bicycle store Copenhagen",
    "Cykelværksted København", "Bicycle repair Copenhagen", "Cykeludlejning København", "Bicycle rental Copenhagen",
    "Elcykel butik København", "Electric bike shop København", "Cykel butik Aarhus", "Bicycle shop Aarhus",
    "Cykelbutik Aarhus", "Bike shop Aarhus", "Cykelværksted Aarhus", "Bicycle repair Aarhus",
    "Cykeludlejning Aarhus", "Bicycle rental Aarhus", "Elcykel butik Aarhus", "Electric bike shop Aarhus",
    "Cykel butik Odense", "Bicycle shop Odense", "Cykelbutik Odense", "Bike shop Odense",
    "Cykelværksted Odense", "Bicycle repair Odense", "Cykeludlejning Odense", "Bicycle rental Odense",
    "Elcykel butik Odense", "Electric bike shop Odense", "Cykel butik Aalborg", "Bicycle shop Aalborg",
    "Cykelbutik Aalborg", "Bike shop Aalborg", "Cykelværksted Aalborg", "Bicycle repair Aalborg",
    "Cykeludlejning Aalborg", "Bicycle rental Aalborg", "Elcykel butik Aalborg", "Electric bike shop Aalborg",
    "Cykel butik Esbjerg", "Bicycle shop Esbjerg", "Cykelbutik Esbjerg", "Bike shop Esbjerg",
    "Cykelværksted Esbjerg", "Bicycle repair Esbjerg", "Cykeludlejning Esbjerg", "Bicycle rental Esbjerg",
    "Cykel butik Randers", "Bicycle shop Randers", "Cykelbutik Randers", "Bike shop Randers",
    "Cykelværksted Randers", "Bicycle repair Randers", "cykel", "cykler", "cykle", "cykelhandel",
    "cykelværksted", "cykeludlejning", "cykelforretning", "cykelmekaniker", "cykelreparation",
    "cykelservice", "cykelcenter", "cykelbutik", "cykel shop", "cycle", "cycles", "bike", "bikes",
    "cycle shop", "bike shop", "bicycle shop", "bicycle repair", "bike repair", "cycle repair",
    "cykel butik i danmark", "CYKELBUTIK I DANMARK", "BICYCLE SHOP DENMARK", "cykel-værksted i Danmark",
    "cykel udlejning", "electric cykel butik"
]

# List of Danish cities and towns (200+ locations)
danish_locations = [
    "Aabenraa", "Aalborg", "Aarhus", "Albertslund", "Allerød", "Assens", "Ballerup", "Billund",
    "Birkerød", "Bjerringbro", "Bogense", "Bording", "Bornholm", "Bramming", "Brande", "Brøndby",
    "Brønderslev", "Brønshøj", "Charlottenlund", "Copenhagen", "Dragør", "Ebeltoft", "Egå",
    "Esbjerg", "Espergærde", "Faaborg", "Farum", "Faxe", "Fensmark", "Fjerritslev", "Fredensborg",
    "Fredericia", "Frederiksberg", "Frederikshavn", "Frederikssund", "Frederiksværk", "Fuglebjerg",
    "Furesø", "Galten", "Gandrup", "Gentofte", "Gilleleje", "Give", "Gladsaxe", "Glostrup",
    "Gram", "Grenaa", "Greve", "Grindsted", "Gudhjem", "Guldborgsund", "Hadsten", "Haderslev",
    "Hals", "Hammel", "Hanstholm", "Hasle", "Haslev", "Havdrup", "Hedehusene", "Hedensted",
    "Hellerup", "Helsingør", "Herlev", "Herning", "Hillerød", "Hinnerup", "Hirtshals", "Hjallerup",
    "Hjørring", "Hobro", "Holbæk", "Holstebro", "Holte", "Horsens", "Humlebæk", "Hundested",
    "Hvidovre", "Hørsholm", "Ikast", "Ishøj", "Jammerbugt", "Jelling", "Juelsminde", "Jyderup",
    "Jyllinge", "Kalundborg", "Karise", "Kastrup", "Kerteminde", "Kibæk", "Kirke Hvalsø", "Kjellerup",
    "Kolding", "Korsør", "København", "Køge", "Langeland", "Langeskov", "Lemvig", "Lejre",
    "Lillerød", "Lind", "Liseleje", "Lolland", "Lyngby", "Lynge", "Løgstør", "Løkken", "Løsning",
    "Mariager", "Maribo", "Middelfart", "Morud", "Måløv", "Nakskov", "Nexø", "Nibe", "Nordborg",
    "Nyborg", "Nykøbing Falster", "Nykøbing Mors", "Nykøbing Sjælland", "Nærum", "Næstved",
    "Nørager", "Nørre Alslev", "Nørresundby", "Odder", "Odense", "Oksbøl", "Otterup", "Padborg",
    "Pandrup", "Præstø", "Randers", "Ribe", "Ringkøbing", "Ringsted", "Risskov", "Roskilde",
    "Rudersdal", "Rungsted", "Rødding", "Rødovre", "Rønde", "Rønne", "Sakskøbing", "Samsø",
    "Silkeborg", "Sindal", "Sjællands Odde", "Skagen", "Skanderborg", "Skibby", "Skive",
    "Skjern", "Skælskør", "Slagelse", "Smørum", "Snekkersten", "Solrød", "Sorø", "Stege",
    "Stenløse", "Stoholm", "Store Heddinge", "Struer", "Støvring", "Sunds", "Svaneke", "Svendborg",
    "Sæby", "Søborg", "Sønderborg", "Søndersø", "Taastrup", "Tarm", "Them", "Thisted",
    "Thyborøn", "Tisvildeleje", "Toftlund", "Tølløse", "Tønder", "Tune", "Tårs", "Ugerløse",
    "Ulfborg", "Vallensbæk", "Vamdrup", "Varde", "Vejby", "Vejen", "Vejle", "Veksø", "Vemb",
    "Vester Hassing", "Vesterborg", "Viborg", "Videbæk", "Vig", "Vildbjerg", "Vinderup",
    "Virum", "Vissenbjerg", "Vojens", "Vordingborg", "Ærøskøbing", "Ølgod", "Ølstykke",
    "Ørbæk", "Ørum Djurs", "Aars", "Åbyhøj", "Åkirkeby", "Årslev"
]

# Generate full list of search terms by combining base_keywords with danish_locations
locations = []
for keyword in base_keywords:
    for loc in danish_locations:
        locations.append(f"{keyword} {loc}")

# Maximum listings per keyword
max_listings =100

# ---------------------------
# Selenium Setup
# ---------------------------
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument('--lang=en-US')  # Set language to English for consistency
driver = webdriver.Chrome(options=chrome_options)

# ---------------------------
# CSV Setup
# ---------------------------
output_file = "denmark_bicycle_shops.csv"
fieldnames = [
    "Keyword", "Name", "Type", "Address", "Phone", "Plus Code",
    "Rating", "Website", "Reviews Count", "Latitude", "Longitude", "Map URL"
]
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

# ---------------------------
# Helper Functions
# ---------------------------
def safe_extract(driver, xpath, timeout=8):
    """Safely extract text from an element with a timeout."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element.text.strip()
    except (TimeoutException, NoSuchElementException):
        return "Not Found"

def get_element_attribute(driver, xpath, attribute, timeout=8):
    """Extract an attribute from an element with a timeout."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element.get_attribute(attribute)
    except (TimeoutException, NoSuchElementException):
        return "Not Found"

def extract_from_aria_label(driver, data_item_id, prefix):
    """Extract text from a button's aria-label, removing the prefix."""
    try:
        element = driver.find_element(By.XPATH, f'//button[@data-item-id="{data_item_id}"]')
        aria_label = element.get_attribute("aria-label")
        if aria_label and aria_label.startswith(prefix):
            return aria_label[len(prefix):].strip()
        return "Not Found"
    except NoSuchElementException:
        return "Not Found"

def clean_text(text):
    """Remove leading non-alphanumeric characters from text."""
    if text and text != "Not Found":
        return re.sub(r"^[^\w\d]+", "", text)
    return text

def extract_phone_number(driver):
    """Extract and standardize phone number from the page."""
    try:
        # Try clickable phone number links (tel: href)
        tel_links = driver.find_elements(By.XPATH, '//a[starts-with(@href, "tel:")]')
        if tel_links:
            phone_text = tel_links[0].text.strip() or tel_links[0].get_attribute('href').replace('tel:', '').strip()
            phone_pattern = r'(\+?\d{1,3})?[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}'
            match = re.search(phone_pattern, phone_text)
            if match:
                cleaned = re.sub(r'[^\d+]', '', match.group())
                return cleaned if cleaned.startswith('+') else '+45' + cleaned
            return "Not Found"
        
        # Fallback: aria-label
        phone = extract_from_aria_label(driver, "phone", "Phone: ")
        if phone != "Not Found":
            return phone
        
        # Fallback: page text
        page_text = safe_extract(driver, '//body')
        phone_pattern = r'(\+?\d{1,3})?[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}'
        match = re.search(phone_pattern, page_text)
        if match:
            cleaned = re.sub(r'[^\d+]', '', match.group())
            return cleaned if cleaned.startswith('+') else '+45' + cleaned
        return "Not Found"
    except:
        return "Not Found"

# ---------------------------
# Scraping Loop
# ---------------------------
for location in locations:
    print(f"\nSearching for: {location}")

    # Navigate to Google Maps
    driver.get("https://www.google.com/maps?hl=en")
    time.sleep(random.uniform(3, 5))

    # Enter search keyword
    try:
        search_box = driver.find_element(By.ID, "searchboxinput")
        search_box.clear()
        search_box.send_keys(location)
        search_box.send_keys(Keys.ENTER)
        time.sleep(random.uniform(5, 7))
    except Exception as e:
        print(f"Error entering search for {location}: {e}")
        continue

    # Scroll to load listings
    try:
        feed = driver.find_element(By.XPATH, '//div[@role="feed"]')
    except NoSuchElementException:
        print(f"No results found for {location}")
        continue

    while True:
        listings = driver.find_elements(By.XPATH, '//a[contains(@href, "/place/")]')
        current_listings = len(listings)
        if current_listings >= max_listings:
            break
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", feed)
        time.sleep(random.uniform(2, 4))
        new_listings = len(driver.find_elements(By.XPATH, '//a[contains(@href, "/place/")]'))
        if new_listings == current_listings:
            if driver.find_elements(By.XPATH, '//p[@class="fontBodyMedium "]//span[text()="You\'ve reached the end of the list."]'):
                print(f"Reached end of list for {location}")
                break

    # Extract unique shop links
    shop_links = driver.find_elements(By.XPATH, '//a[contains(@href, "/place/")]')
    unique_links = list(set([shop.get_attribute("href") for shop in shop_links if "/place/" in shop.get_attribute("href")]))[:max_listings]
    print(f"Found {len(unique_links)} shops for {location}")

    # Loop through each shop link
    for shop_link in unique_links:
        try:
            driver.get(shop_link)
            time.sleep(random.uniform(5, 8))

            # Extract shop name
            name = safe_extract(driver, '//div[@style="padding-bottom: 4px;"]//h1')

            # Extract type
            type_ = safe_extract(driver, '//div[@class="LBgpqf"]//button[@class="DkEaL "]')

            # Extract address
            address = extract_from_aria_label(driver, "address", "Address: ")
            address = clean_text(address) if address else "Not Found"

            # Extract phone number
            phone = extract_phone_number(driver)

            # Extract plus code
            plus_code = extract_from_aria_label(driver, "oloc", "Plus code: ")
            plus_code = clean_text(plus_code) if plus_code else "Not Found"

            # Extract rating
            rating = safe_extract(driver, '//div[@style="padding-bottom: 4px;"]//div[contains(@jslog,"mutable:true;")]/span[1]/span[1]')

            # Extract website
            website = get_element_attribute(driver, '//a[@data-value="Open website"]', 'href')

            # Extract reviews count
            review_raw = safe_extract(driver, '//div[@style="padding-bottom: 4px;"]//div[contains(@jslog,"mutable:true;")]/span[2]')
            reviews_count = re.sub(r'[^\d]', '', review_raw) if review_raw else "Not Found"

            # Extract latitude and longitude from current URL
            try:
                current_url = driver.current_url
                if "/@" in current_url:
                    latlng_part = current_url.split("/@")[1].split(",")
                    latitude = latlng_part[0]
                    longitude = latlng_part[1]
                else:
                    latitude = longitude = "Not Found"
            except:
                latitude = longitude = "Error"

            # Extract map URL
            map_url = shop_link

            # Save data to CSV
            with open(output_file, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writerow({
                    "Keyword": location,
                    "Name": name,
                    "Type": type_,
                    "Address": address,
                    "Phone": phone,
                    "Plus Code": plus_code,
                    "Rating": rating,
                    "Website": website,
                    "Reviews Count": reviews_count,
                    "Latitude": latitude,
                    "Longitude": longitude,
                    "Map URL": map_url
                })

            print(f"Saved: {name} | Lat: {latitude}, Lon: {longitude}")
            time.sleep(random.uniform(3, 5))

        except Exception as e:
            print(f"Error processing {shop_link}: {e}")

print("\n✅ All data collected and saved to CSV")

# ---------------------------
# Close Browser
# ---------------------------
driver.quit()