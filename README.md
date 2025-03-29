# Denmark Bicycle Shops Google Maps Scraper

This project is a Python-based web scraper that uses Selenium to collect data about bicycle shops across Denmark from Google Maps. The scraper leverages an extensive list of keywords—including Danish and English variations with different accents—to ensure maximum coverage. The extracted data includes key details like shop name, address, phone number, rating, reviews count, plus code, and geographic coordinates.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Notes](#notes)
- [License](#license)
- [Contact](#contact)

## Features

- **Extensive Keyword Coverage:**  
  Combines multiple Danish and English keywords to capture every possible cycle shop in Denmark.
  
- **Data Extraction:**  
  Scrapes the following details from Google Maps:
  - **Shop Name**
  - **Address** (including postal code)
  - **Open/Close Time**
  - **Phone Number** (standardized for Denmark; starts with `+45`)
  - **Plus Code**
  - **Rating** (one decimal digit between 1.0 and 5.9)
  - **Reviews Count**
  - **Latitude & Longitude** (extracted from the URL)
  - **Map URL**

- **Lazy Loading & Random Delays:**  
  Mimics human browsing by applying random sleep intervals and scrolling behavior to ensure maximum data capture without triggering Google’s anti-scraping measures.

- **CSV Output:**  
  All extracted data is saved in a well-structured CSV file for easy analysis.

## Prerequisites

Before running this project, ensure you have the following:

- **Python 3.8+**  
  [Download Python](https://www.python.org/downloads/)

- **Google Chrome Browser** installed.

- **ChromeDriver:**  
  Download the ChromeDriver that matches your version of Chrome from [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads) and either place it in your project directory or add it to your system PATH.

- **Python Dependencies:**  
  Install the required Python package by running:
  
  ```bash
  pip install -r requirements.txt
  ```
  
  *The `requirements.txt` file includes:*
  
  ```txt
  selenium>=4.10.0
  ```

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Waqas56jb/Denmark-Bicycles-Google-Map-DataScrapping-Using-Seleinum-.git
   cd Denmark-Bicycles-Google-Map-DataScrapping-Using-Seleinum-
   ```

2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up ChromeDriver:**  
   Ensure that `chromedriver.exe` is available in your project directory or added to your PATH.

## Usage

1. **Customize Keywords (Optional):**  
   The scraper uses an extensive list of keywords defined in the script. You can modify the keyword list to add more variations if needed.

2. **Run the Script:**

   ```bash
   python main.py
   ```

   The script will:
   - Open Google Maps.
   - Search for each keyword (e.g., "Cykelbutik i Danmark", "Bicycle shop Denmark", etc.).
   - Scroll through the listings to load results.
   - Visit each shop’s detail page.
   - Extract relevant information.
   - Save all data into a CSV file named `denmark_bicycle_shops.csv`.

## Project Structure

```
.
├── main.py                  # Main scraping script
├── requirements.txt         # Python dependencies
├── output/                  # Directory where CSV files are saved (created automatically)
└── README.md                # Project documentation (this file)
```

## Configuration

- **Keywords:**  
  The keyword list is built by combining base keywords and a list of Danish cities/towns. You can extend these lists to improve data coverage.

- **Max Listings:**  
  The variable `max_listings` determines how many shops are scraped per keyword. You can adjust this value as needed.

- **Delays:**  
  Random sleep intervals are used throughout the script to mimic human behavior and avoid detection by Google.

## Notes

- **Data Limitations:**  
  Some information (e.g., email addresses or social media links) is not available on Google Maps and will be left blank.
  
- **Dynamic Content:**  
  Google Maps’ layout may change over time. If extraction fails, inspect the page with developer tools and update the XPath selectors accordingly.

- **Ethical Considerations:**  
  Please ensure that your scraping activities comply with Google’s Terms of Service and local regulations. Use the data responsibly.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or support, feel free to contact:
- **Email:** waqas56jb@gmail.com
- **GitHub:** [Waqas56jb](https://github.com/Waqas56jb)

Happy Scraping! 🚴‍♂️