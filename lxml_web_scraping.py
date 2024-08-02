from lxml import html
import requests
import pandas as pd
import logging

# Set up logging configuration
logging.basicConfig(
    filename='lxml_scraper.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# URL to scrape
url = 'https://www.gsmarena.com/apple-phones-48.php'

try:
    # Send an HTTP request
    logging.info('Sending HTTP request to %s', url)
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Parse the HTML content
    logging.info('Parsing HTML content')
    tree = html.fromstring(response.content)

    # Extract data
    logging.info('Extracting data from the HTML content')
    model_list = tree.xpath('//div[@class="makers"]/ul/li')

    models = []
    links = []
    details = []
    
    base_url = 'https://www.gsmarena.com/'

    for model in model_list:
        # Extract the model name
        model_name = model.xpath('.//span/text()')
        if model_name:
            models.append(model_name[0].strip())
        else:
            models.append('')

        # Extract the link associated with the model
        relative_link = model.xpath('.//a/@href')
        if relative_link:
            full_link = base_url + relative_link[0]
            links.append(full_link)
        else:
            links.append('')

        # Extract details about the model
        model_detail = model.xpath('.//a/img/@title')
        if model_detail:
            details.append(model_detail[0])
        else:
            details.append('')

    # Display the extracted models, links, and details
    print("Models:", models)
    print("Links:", links)
    print("Details:", details)
    
    # Log the extracted data count
    logging.info(f'Extracted {len(models)} models.')

    # Prepare data for saving
    data = {
        'Model': models,
        'Link': links,
        'Detail': details
    }

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Save to Excel, CSV, and JSON
    df.to_excel('lxml_extracted_data.xlsx', index=False, engine='openpyxl')
    df.to_csv('lxml_extracted_data.csv', index=False)
    df.to_json('lxml_extracted_data.json', orient='records', indent=4)

    logging.info("Data has been saved to Excel, CSV, and JSON files.")
    print("Data has been saved to Excel, CSV, and JSON files.")

except Exception as e:
    logging.error('An unexpected error occurred: %s', e)
