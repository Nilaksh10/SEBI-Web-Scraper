from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from selenium.webdriver.chrome.options import Options

  

driver = webdriver.Chrome()

url = "https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doPmr=yes"
driver.get(url)

WebDriverWait(driver, 0.5).until(
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
    pm_dropdown = Select(driver.find_element(By.NAME, 'pmrId'))
    pm_options = pm_dropdown.options

    for pm_index in range(1, len(pm_options)):  
        pm_dropdown = Select(driver.find_element(By.NAME, 'pmrId'))
        pm_name = pm_dropdown.options[pm_index].text.strip()
        pm_dropdown.select_by_index(pm_index)
        WebDriverWait(driver, 0.5).until(
            EC.presence_of_element_located((By.NAME, 'month'))
        )
        month_dropdown = Select(driver.find_element(By.NAME, 'month'))

        for month_index in range(1, len(month_dropdown.options)):  
            month_dropdown = Select(driver.find_element(By.NAME, 'month'))
            month_name = month_dropdown.options[month_index].text.strip()
            month_dropdown.select_by_index(month_index)

           
            WebDriverWait(driver, 0.5).until(
                EC.presence_of_element_located((By.NAME, 'year'))
            )
            year_dropdown = Select(driver.find_element(By.NAME, 'year'))

            for year_index in range(1, len(year_dropdown.options)):  
                year_dropdown = Select(driver.find_element(By.NAME, 'year'))
                year_name = year_dropdown.options[year_index].text.strip()
                year_dropdown.select_by_index(year_index)

               
                go_button = driver.find_element(By.CLASS_NAME, "go-search")
                go_button.click()

              
                try:
                    WebDriverWait(driver, 0.5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'statistics-table'))
                    )
                except:
                    print(f"No data for {pm_name} - {month_name} - {year_name}, skipping...")
                    continue

               
                tables = driver.find_elements(By.CLASS_NAME, 'statistics-table')

                for table_index, table in enumerate(tables):
                    rows = table.find_elements(By.TAG_NAME, 'tr')

                    for row in rows:
                        cols = row.find_elements(By.TAG_NAME, 'td')
                        if len(cols) > 0:
                            row_data = [col.text.strip() for col in cols]
                            row_data.insert(0, f"Table {table_index + 1}")  # Table index
                            row_data.insert(0, year_name)
                            row_data.insert(0, month_name)
                            row_data.insert(0, pm_name)
                            data.append(row_data)

             
                driver.find_element(By.NAME, 'pmrId').click()
                driver.find_element(By.NAME, 'month').click()
                driver.find_element(By.NAME, 'year').click()

except Exception as e:
    print("An error occurred:", e)

finally:
    df = pd.DataFrame(data, columns=headers)
    df.to_csv('sebi_pms_data.csv', index=False)
    print("Data saved to 'sebi_pms_data.csv'.")

    
    driver.quit() 