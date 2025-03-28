# 🚲 Denmark Bicycle Shops Scraper (Google Maps Data Collection)

This project will automatically collect all information about bicycle shops in Denmark using Selenium and save the data into a CSV file for data analysis.

---

## ✅ Features

- Scrapes ALL Google Maps bicycle shop data
- Handles lazy-loading, dynamic content, and errors automatically
- Collects:
    - Shop Name
    - Address
    - Plus Code
    - Latitude / Longitude
    - Phone Number
    - Website
    - Opening Hours
    - Status (Open/Closed)
    - Category
    - Rating
    - Number of Reviews
    - Photos
    - Reviews (Optional)
    - Google Map URL
    - And more...
- Saves everything into a clean CSV file
- Designed for data scientists and analysts

---

## 💻 Requirements

Before running the scraper, you need to install the following:

1. Python 3.8+
2. Google Chrome Browser
3. ChromeDriver (compatible with your Chrome version)  
   Download from: https://chromedriver.chromium.org/downloads

---

## 📦 Python Libraries

Required Python libraries are listed in `requirements.txt`

Install them using:

```bash
pip install -r requirements.txt
```

---

## ✅ Setup (Step by Step)

### Step 1: Download & Install ChromeDriver

- Go to [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)
- Download the version matching your installed Chrome browser
- Extract it and place `chromedriver.exe` into the project folder (or add to system PATH)

---

### Step 2: Clone this Repository (or copy files manually)

```bash
git clone https://github.com/Waqas56jb/Denmark-Bicycles-Google-Map-DataScrapping-Using-Seleinum-.git
cd Denmark-Bicycles-Google-Map-DataScrapping-Using-Seleinum
```

Or just download the files and place them into a folder.

---

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 4: Configure Keywords

Open `main.py` (or the scraper script) and set the keyword list you want to search:

```python
keywords = [
    "Cykelbutik i Danmark",
    "Bicycle shop Denmark",
    ...
]
```

---

### Step 5: Run the Scraper

```bash
python Bicycle Data Scrapper.py
```

---

### Step 6: Output

After successful scraping, you will get:

```bash
output/bicycle_shops.csv
```

It will contain all the collected data.

---

## ✅ Notes

- The script handles:
    - Lazy loading
    - Scrolling automatically
    - Sleep/delay to mimic human behavior
    - Multiple keywords search
    - CSV export
    
- It will automatically avoid soft Google Map blocking (undetected-chromedriver + user-agent rotation)

---

## ⚠️ Important

- Don't overload Google Maps (keep reasonable delay)
- Respect scraping ethics
- Avoid running continuously for hours without pause
- You are responsible for how you use the collected data

---

## 💡 Recommended

If you plan to scrape 10,000+ records:
- Use a VPN with rotation
- Increase `sleep()` delays inside the code
- Handle captchas if they appear (you can extend the code)

---

If you want, I can also give you:
✅ Captcha Detection  
✅ Auto-retry on Error  
✅ Headless Option  
✅ Large Dataset Optimizer  
✅ Ready-to-use Dockerfile

Just reply **yes make it full** and I will prepare the complete production-level scraper with instructions for you.

---