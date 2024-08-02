import scrapy
import pandas as pd

class MySpider(scrapy.Spider):
    name = 'my_spider'
    start_urls = ['https://www.gsmarena.com/apple-phones-48.php']

    def parse(self, response):
        # base_url = 'https://www.gsmarena.com/'
        model_list = response.css('div.makers ul li')
        
        # Lists to store the extracted data
        models = []
        links = []
        details = []

        for model in model_list:
            # Extract the model name
            model_name = model.css('span::text').get().strip()
            models.append(model_name)

            # Extract the link associated with the model
            relative_link = model.css('a::attr(href)').get()
            full_link = response.urljoin(relative_link)  # Convert to full URL
            links.append(full_link)

            # Extract details about the model
            model_detail = model.css('a img::attr(title)').get()
            details.append(model_detail)

            # Yield the extracted data
            yield {
                'Model': model_name,
                'Link': full_link,
                'Detail': model_detail
            }

        # Save data to a DataFrame
        data = {
            'Model': models,
            'Link': links,
            'Detail': details
        }
        df = pd.DataFrame(data)

        # Save to Excel, CSV, and JSON
        df.to_excel('scrapy_extracted_data.xlsx', index=False, engine='openpyxl')
        df.to_csv('scrapy_extracted_data.csv', index=False)
        df.to_json('scrapy_extracted_data.json', orient='records', indent=4)

        self.logger.info("Data has been saved to Excel, CSV, and JSON files.")

        # To log the process
        self.logger.info('Data extraction completed.')
