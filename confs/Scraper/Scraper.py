from selenium.webdriver.common.by import By
from confs.Scraper.Selenium import Selenium

class Scraper(Selenium):
    def __init__(self, driver):
        self.driver = driver

    def scrape_data(self, config):
        try:
            table_data = []
            return self.scrape_custom_data(config, table_data)
        except Exception as e:
            print(f"Error al extraer la información: {e}")

    def scrape_custom_data(self, config, table_data):
        try:
            main_element = self.driver
            if 'main_element_selector' in config:
                main_element = self.element(config['main_element_selector'])
            rows = main_element.find_elements(By.CSS_SELECTOR, config['row_selector'])
            
            for i in range(min(config.get('num_items', len(rows)), len(rows))):
                row = rows[i]
                row_data = {}
                for field, selector in config['fields'].items():
                    elements = row.find_elements(By.CSS_SELECTOR, selector)
                    row_data[field] = elements[0].text.strip() if elements else None
                table_data.append(row_data)
            return table_data
        except Exception as e:
            print(f"Error al extraer información personalizada: {e}")