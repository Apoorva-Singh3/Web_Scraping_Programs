import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging

url = 'https://www.gsmarena.com/apple-phones-48.php'

# Set up logging configuration
logging.basicConfig(
    filename='requests&beautifulsoup.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

try:
    
    # Log the start of the data extraction process
    logging.info('Data extraction started...')
    
    # Step 1: Send an HTTP request to the website
    response = requests.get(url)

    # Step 2: Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Step 3: Extract data
    # Extracting phone models and their corresponding links
    model_list = soup.find('div', class_='makers').find_all('li')
    models = []
    links = []
    details = []

    base_url = 'https://www.gsmarena.com/'

    for model in model_list:
        # Extract the model name
        model_name = model.find('span').text.strip()
        models.append(model_name)

        # Extract the link associated with the model
        link = model.find('a')['href']  # Get the href attribute of the <a> tag
        full_link = base_url + link  # Create the full URL
        links.append(full_link)
        
        #Extract details about the model
        model_detail = model.find('a').find('img')['title']
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
    df.to_excel('/home/apoorva/Web_Scraping_Programs/requests&beautifulsoup_extracted_data.xlsx', index=False, engine='openpyxl')

    print("Data has been saved to 'requests&beautifulsoup_extracted_data.xlsx'")

    df.to_csv('/home/apoorva/Web_Scraping_Programs/requests&beautifulsoup_extracted_data.csv', index=False)
    # df.to_csv('/home/apoorva/Web_Scraping_Programs/requests&beautifulsoup_extracted_data.csv', index=False, header=False)
    # df.to_csv('/home/apoorva/Web_Scraping_Programs/requests&beautifulsoup_extracted_data.csv', columns=['Models', 'Details', 'Links'], index=False)

    print("Data has been saved to 'requests&beautifulsoup_extracted_data.csv'")
    
    json_file_path = '/home/apoorva/Web_Scraping_Programs/requests&beautifulsoup_extracted_data.json'
    df.to_json(json_file_path, orient='records', indent=4)
    # df.to_json(json_file_path, orient='columns', indent=4)
    # df.to_json(json_file_path, orient='split', indent=4)
    # df.to_json(json_file_path, orient='index', indent=4)    

    print(f"Data has been saved to '{json_file_path}'")
    
except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
    
# Log your processes
logging.info('Data has been saved')