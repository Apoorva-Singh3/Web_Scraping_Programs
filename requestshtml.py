from requests_html import HTMLSession
import pandas as pd
import logging

# Set up logging configuration
logging.basicConfig(
    filename='requests_html.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def scrape_gsmarena():
    try:
        # Create an HTML session
        session = HTMLSession()

        # Send a request and render JavaScript
        response = session.get('https://www.gsmarena.com/apple-phones-48.php')
        response.html.render(sleep=1)  # Allow time for JavaScript to render

        # Log the start of the data extraction process
        logging.info('Data extraction started...')

        # Extract data
        model_list = response.html.find('div.makers ul li')

        # Lists to store extracted data
        models = []
        links = []
        details = []

        base_url = 'https://www.gsmarena.com/'

        for model in model_list:
            # Extract the model name
            model_name = model.find('span', first=True).text.strip()
            models.append(model_name)

            # Extract the link associated with the model
            relative_link = model.find('a', first=True).attrs['href']
            full_link = base_url + relative_link  # Construct the full URL
            links.append(full_link)

            # Extract details about the model
            model_detail = model.find('a img', first=True).attrs['title']
            details.append(model_detail)

            # Log each model's data
            logging.info(f'Extracted model: {model_name}, Link: {full_link}, Details: {model_detail}')

        # Display the extracted models and links
        print("Models:", models)
        print("Links:", links)
        print("Details:", details)

        # Prepare data for Excel, CSV, and JSON
        data = {
            'Models': models,
            'Links': links,
            'Details': details
        }

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Save to Excel
        df.to_excel('requests_html_extracted_data.xlsx', index=False, engine='openpyxl')
        print("Data has been saved to 'requests_html_extracted_data.xlsx'")

        # Save to CSV
        df.to_csv('requests_html_extracted_data.csv', index=False)
        print("Data has been saved to 'requests_html_extracted_data.csv'")

        # Save to JSON
        json_file_path = 'requests_html_extracted_data.json'
        df.to_json(json_file_path, orient='records', indent=4)
        print(f"Data has been saved to '{json_file_path}'")

        # Log the completion of the data extraction
        logging.info('Data extraction completed and saved to files.')

    except Exception as e:
        print(f"Error fetching data: {e}")
        logging.error(f"Error fetching data: {e}")

# Run the scrape function
scrape_gsmarena()
