from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import pandas as pd
import logging
import time

# Set up logging configuration
logging.basicConfig(
    filename='selenium_scraping.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Set up the WebDriver using WebDriver Manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Set up the WebDriver using WebDriver Manager for Firefox
# driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

# Set up the WebDriver using WebDriver Manager for Edge
# driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))

# Open the webpage
driver.get('https://www.gsmarena.com/apple-phones-48.php')

# Wait for the page to load completely
# time.sleep(3)  # Pause for 3 seconds to ensure the page loads fully

# Wait until a specific element is found (up to 10 seconds)
try:
    # Wait for the heading to be present
    heading_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'h1'))
    )

    # Extract phone models and links
    model_list = driver.find_elements(By.CSS_SELECTOR, 'div.makers li')
    models = []
    links = []
    details = []

    base_url = 'https://www.gsmarena.com/'

    for model in model_list:
        # Extract the model name
        model_name = model.find_element(By.TAG_NAME, 'span').text.strip()
        models.append(model_name)

        # Extract the link associated with the model
        link_element = model.find_element(By.TAG_NAME, 'a')
        link = link_element.get_attribute('href')
        links.append(link)

        # Extract details about the model
        model_detail = link_element.find_element(By.TAG_NAME, 'img').get_attribute('title')
        details.append(model_detail)

    # Display the extracted models and links
    print("Models:", models)
    print("Links:", links)
    print("Details:", details)

    # Step 4: Prepare data for Excel
    data = {
        'Models': models,
        'Links': links,
        'Details': details
    }

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Step 5: Save to Excel, CSV & JSON
    df.to_excel('/home/apoorva/Web_Scraping_Programs/selenium_extracted_data.xlsx', index=False, engine='openpyxl')
    
    df.to_csv('/home/apoorva/Web_Scraping_Programs/selenium_extracted_data.csv', index=False)
        
    json_file_path = '/home/apoorva/Web_Scraping_Programs/selenium_extracted_data.json'
    df.to_json(json_file_path, orient='records', indent=4)
    
    print(f"Data has been saved to '{json_file_path}'")
    logging.info('Data has been saved')
    
except Exception as e:
    print("An error occurred:", e)

finally:
    # Close the WebDriver
    driver.quit()
