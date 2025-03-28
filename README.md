Denmark Bicycle Shops Google Maps Scraper
This project uses Selenium to automatically scrape Google Maps for Denmark bicycle shop information. It covers multiple Danish and English search keywords and location combinations so that you capture as many cycle shop listings as possible. The scraper visits each shop detail page, extracts key information, and saves it into a CSV file.

Table of Contents
Features

Prerequisites

Installation

Usage

Project Structure

Configuration

Notes

License

Features
Multi-language & Extensive Keywords:
Searches using a comprehensive list of Danish and English keywords, including variations for “cykelbutik”, “bicycle shop”, “cykelværksted”, “bike repair”, and more.

Dynamic Data Extraction:
Visits each shop’s Google Maps detail page and extracts the following fields:

Name: The shop/business name.

Address: Full address including postal code.

Open/Close Time: Operating status and hours.

Phone: Denmark phone number (formatted to start with +45).

Plus Code: Unique location identifier (if available).

Rating: Business rating (e.g., "4.8", one decimal digit).

Reviews Count: Number of reviews (extracted from text like "(45)").

Latitude/Longitude: Extracted from the URL.

Map URL: The detail page URL.

CSV Output:
All extracted data is saved into a CSV file for easy analysis.

Lazy Loading & Random Delays:
Uses randomized sleep intervals and scrolling to load dynamic content and avoid detection by Google.

Prerequisites
Before you begin, please ensure you have the following:

Python 3.8+
Download Python

Google Chrome Browser installed.

ChromeDriver:
Download the ChromeDriver that matches your Chrome version from ChromeDriver Downloads and either place it in your project folder or add it to your system PATH.

Python Packages:
You need the Selenium package. Install it via pip:

 
pip install selenium
Installation
Clone the repository:

 
git clone https://github.com/Waqas56jb/Denmark-Bicycles-Google-Map-DataScrapping-Using-Seleinum-.git
cd Denmark-Bicycles-Google-Map-DataScrapping-Using-Seleinum-
Install Dependencies:

Create a requirements.txt file (if not already provided) with at least:

 
selenium>=4.0.0
And install the dependencies:

 
pip install -r requirements.txt
Set Up ChromeDriver:
Ensure your ChromeDriver is in your project directory or added to the PATH.

Usage
Customize Keyword Lists (Optional):

The keywords are defined in main.py as two lists:

base_keywords: Generic Danish and English terms.

danish_locations: A list of over 200 Danish cities and towns.

The script automatically combines these lists to generate an extensive set of search queries.

Run the Scraper:

Run the main script:
 
python main.py
The scraper will:

Open Google Maps.

Loop through every combined search query.

Scroll the results panel to load shop listings.

Click each listing to extract detailed information.

Save all data into a CSV file named denmark_bicycle_shops.csv.

Project Structure
 
├── main.py               # Main scraping script
├── README.md             # Project documentation (this file)
├── requirements.txt      # Python dependencies (e.g., selenium)
└── csv file              # Directory where CSV files are saved (created automatically)
Configuration
Keywords:
The keyword generation is done by combining base_keywords and danish_locations. You can edit these lists in main.py to add more variations or cover additional regions.

Max Listings:
The variable max_listings controls how many shops to scrape per search query. Adjust this number as needed.

Random Delays:
Random sleep intervals are used throughout the script to mimic human behavior and reduce the chance of being blocked by Google.

Notes
Data Limitations:
Some information (such as email addresses and social media links) is not provided by Google Maps and will be left blank.

Dynamic Content:
Google Maps uses dynamic loading. If you notice missing data, you may need to increase the sleep duration or adjust the scrolling loops.

Future Extensions:
You can extend the code to automatically handle pagination (scrolling beyond the initial results) or integrate more detailed parsing if Google changes its DOM structure.

Disclaimer:
Scraping data from Google Maps may violate their Terms of Service. Use this tool responsibly and only for permitted purposes.

License
This project is provided under the MIT License.

If you have any questions or need further customization, feel free to open an issue or contact me at waqas56jb@gmail.com.

Happy Scraping! 🚴‍♂️