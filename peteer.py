import asyncio
from pyppeteer import launch
import pandas as pd
import logging

# Set up logging configuration
logging.basicConfig(
    filename='pyppeteer_extraction.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def main():
    try:
        # Log the start of the data extraction process
        logging.info('Data extraction started...')

        # Launch a headless browser
        browser = await launch(headless=True, args=['--no-sandbox'])
        page = await browser.newPage()

        # Open the webpage
        await page.goto('https://www.gsmarena.com/apple-phones-48.php', waitUntil='domcontentloaded')

        # Extract data
        # Extract phone models, links, and details
        model_elements = await page.querySelectorAll('div.makers ul li')
        
        # Lists to store extracted data
        models = []
        links = []
        details = []

        for model in model_elements:
            # Extract the model name
            model_name = await page.evaluate('(element) => element.querySelector("span").textContent', model)
            models.append(model_name.strip())

            # Extract the link associated with the model
            relative_link = await page.evaluate('(element) => element.querySelector("a").getAttribute("href")', model)
            full_link = page.url + relative_link
            links.append(full_link)

            # Extract details about the model
            model_detail = await page.evaluate('(element) => element.querySelector("a img").getAttribute("title")', model)
            details.append(model_detail)

        # Close the browser
        await browser.close()

        # Display the extracted models, links, and details
        print("Models:", models)
        print("Links:", links)
        print("Details:", details)

        # Log the extracted data count
        logging.info(f'Extracted {len(models)} models.')

        # Step 4: Prepare data for Excel, CSV & JSON
        data = {
            'Models': models,
            'Links': links,
            'Details': details
        }

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Save to Excel, CSV, and JSON
        df.to_excel('pyppeteer_extracted_data.xlsx', index=False, engine='openpyxl')
        df.to_csv('pyppeteer_extracted_data.csv', index=False)
        df.to_json('pyppeteer_extracted_data.json', orient='records', indent=4)

        # Log successful data saving
        logging.info("Data has been saved to Excel, CSV, and JSON files.")
        print("Data has been saved to Excel, CSV, and JSON files.")

    except Exception as e:
        logging.error(f'An error occurred: {e}')
        print(f'An error occurred: {e}')

# Run the script
asyncio.get_event_loop().run_until_complete(main())
