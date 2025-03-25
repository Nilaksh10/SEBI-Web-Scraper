from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Initialize the driver
driver = webdriver.Chrome()
url = "https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doPmr=yes"
driver.get(url)

# Wait for page to load properly
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.NAME, 'pmrId'))
)

data = []

headers = [
    "Portfolio Manager", "Month", "Year", "Table Index",
    "Company Name", 
    "Clients (Domestic PF/EPFO)", "Clients (Domestic Corporates)", "Clients (Domestic Non-Corporates)", 
    "Clients (Foreign Non-Residents)", "Clients (Foreign FPI)", "Clients (Foreign Others)",
    "AUM (Domestic PF/EPFO)", "AUM (Domestic Corporates)", "AUM (Domestic Non-Corporates)", 
    "AUM (Foreign Non-Residents)", "AUM (Foreign FPI)", "AUM (Foreign Others)"
]

try:
    # Get portfolio managers dropdown
    pm_dropdown = Select(driver.find_element(By.NAME, 'pmrId'))
    pm_options = pm_dropdown.options
    
    # Limit to first 2 PMs for testing (remove in production)
    for pm_index in range(1, min(3, len(pm_options))):  # Start from 1 to skip default option
        pm_dropdown = Select(driver.find_element(By.NAME, 'pmrId'))
        pm_name = pm_dropdown.options[pm_index].text.strip()
        print(f"\nProcessing Portfolio Manager: {pm_name}")
        pm_dropdown.select_by_index(pm_index)
        time.sleep(2)  # Allow dropdown to update
        
        # Get month dropdown
        month_dropdown = Select(WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'month'))
        ))
        
        for month_index in range(1, len(month_dropdown.options)):  # Start from 1 to skip default
            month_dropdown = Select(driver.find_element(By.NAME, 'month'))
            month_name = month_dropdown.options[month_index].text.strip()
            print(f"  Processing Month: {month_name}")
            month_dropdown.select_by_index(month_index)
            time.sleep(1)  # Allow dropdown to update
            
            # Get year dropdown
            year_dropdown = Select(WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'year'))
            ))
            
            for year_index in range(1, len(year_dropdown.options)):  # Start from 1 to skip default
                year_dropdown = Select(driver.find_element(By.NAME, 'year'))
                year_name = year_dropdown.options[year_index].text.strip()
                print(f"    Processing Year: {year_name}", end=" ")
                year_dropdown.select_by_index(year_index)
                time.sleep(1)  # Allow dropdown to update
                
                # Click the Go button
                go_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "go-search"))
                )
                go_button.click()
                
                # Wait for either data or "No Data" message
                try:
                    # First check for "No Data" message
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'No Data')]"))
                    )
                    print("- No data available")
                    continue
                except:
                    # If no "No Data" message, look for tables
                    try:
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'statistics-table'))
                        )
                        print("- Data found")
                        
                        # Process all tables on the page
                        tables = driver.find_elements(By.CLASS_NAME, 'statistics-table')
                        
                        for table_index, table in enumerate(tables):
                            rows = table.find_elements(By.TAG_NAME, 'tr')
                            
                            # Skip header row if it contains column names
                            start_row = 1 if any('Company Name' in row.text for row in rows[:1]) else 0
                            
                            for row in rows[start_row:]:
                                cols = row.find_elements(By.TAG_NAME, 'td')
                                if len(cols) >= 13:  # Ensure we have enough columns
                                    row_data = [col.text.strip() for col in cols]
                                    # Insert metadata at beginning
                                    row_data.insert(0, f"Table {table_index + 1}")  # Table index
                                    row_data.insert(0, year_name)
                                    row_data.insert(0, month_name)
                                    row_data.insert(0, pm_name)
                                    data.append(row_data)
                    
                    except Exception as table_error:
                        print(f"- Error loading table: {str(table_error)}")
                        continue
                
                # Go back to the search form
                driver.back()
                # Wait for form to reload
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, 'pmrId'))
                )
                # Re-select the dropdowns
                pm_dropdown = Select(driver.find_element(By.NAME, 'pmrId'))
                pm_dropdown.select_by_index(pm_index)
                time.sleep(1)
                month_dropdown = Select(driver.find_element(By.NAME, 'month'))
                month_dropdown.select_by_index(month_index)
                time.sleep(1)
                year_dropdown = Select(driver.find_element(By.NAME, 'year'))
                year_dropdown.select_by_index(year_index)
                time.sleep(1)

except Exception as e:
    print("\nAn error occurred:", e)
    # Take screenshot for debugging
    driver.save_screenshot('error_screenshot.png')
    raise e  # Re-raise the error after logging

finally:
    if data:
        df = pd.DataFrame(data, columns=headers)
        df.to_csv('sebi_pms_data.csv', index=False)
        print(f"\nSuccess! Data saved to 'sebi_pms_data.csv'. Found {len(data)} records.")
    else:
        print("\nNo data was scraped.")
    
    driver.quit()