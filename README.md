# SEBI Web Scraper

## Project Overview

The **SEBI Portfolio Managers Data Scraping** project is designed to collect and analyze data from the SEBI website. The extracted data provides insights into the performance of **512 portfolio managers** for **June 2024**. This project uses **Python-based web scraping techniques** to automate data extraction, cleaning, and organization for further analysis.

## Tech Stack Used

- **Python**: For automating web scraping and data extraction.
- **Selenium**: For web automation and data extraction.
- **Pandas**: For data manipulation and processing.
- **Excel (CSV format)**: For structuring and analyzing data.

## Prerequisites

Ensure you have the following installed on your system:

- **Python (>=3.8)**
- **pip** (Python package manager)
- **Google Chrome** and **ChromeDriver** (matching your Chrome version)
- **Virtual environment** (optional but recommended)

## Installation & Setup

### 1. Clone the Repository

```sh
git clone https://github.com/Nilaksh10/SEBI-Web-Scraper.git
cd SEBI-Web-Scraper
```

### 2. Create a Virtual Environment (Optional)

```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

If `requirements.txt` is missing, manually install dependencies:

```sh
pip install selenium pandas
```

## Running the Web Scraper

### 1. Run the Scraper Script

```sh
python SebiScrappy.py
```
### It has a small issue as SEBI has changed their website they currently dont allow scrapers to get data so you would just need to press the GO button once when the Selenium script is running on the chrome browser and then the scraping will start(SEBI changed it after this project was made...)

#### This script will:
- Use **Selenium** to navigate the SEBI Portfolio Managers website.
- Extract relevant attributes for each portfolio manager.
- Save the raw data to `sebi_pms_data.csv`.

### 2. Clean the Extracted Data

```sh
python cleancsv.py
```

#### This script will:
- Clean missing or duplicate entries.
- Format and structure the data.
- Save the cleaned data as `sebi_pms_data_cleaned.csv`.

## Output Files

- **`sebi_pms_data.csv`**: The raw extracted data.
- **`sebi_pms_data_cleaned.csv`**: The cleaned and processed dataset for analysis.



## Future Enhancements

- Automate periodic data scraping for real-time updates.
- Use machine learning models for predictive analysis.
- Develop interactive dashboards for better visualization.

---

**Author:** Nilaksh10  
**License:** MIT  
**GitHub Repository:** [SEBI-Web-Scraper](https://github.com/Nilaksh10/SEBI-Web-Scraper)
