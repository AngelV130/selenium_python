from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

class Scraper:
    def __init__(self, config):
        self.config = config
        self.options = Options()
        self.options.headless = False
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.options)

    def navigate_to_page(self):
        try:
            self.driver.get(self.config['url'])
            return self.perform_actions()
        except Exception as e:
            print(f"Error al cargar la página: {e}")

    def perform_actions(self):
        try:
            if 'actions' in self.config:
                for action in self.config['actions']:
                    element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, action['selector'])))
                    if action['type'] == 'click':
                        element.click()
                    elif action['type'] == 'input':
                        element.send_keys(action['value'])
                    elif action['type'] == 'select':
                        for option in element.find_elements(By.TAG_NAME, 'option'):
                            if option.text == action['value']:
                                option.click()
                                break
                    elif action['type'] == 'submit':
                        element.send_keys(Keys.RETURN)
            return self.scrape_data()
        except Exception as e:
            print(f"Error al realizar las acciones: {e}")

    def scrape_data(self):
        try:
            table_data = []
            if 'fields' in self.config:
                self.scrape_custom_data(table_data)
            else:
                self.scrape_generic_data(table_data)
            return self.create_data(table_data)
        except Exception as e:
            print(f"Error al extraer la información: {e}")

    def scrape_generic_data(self, table_data):
        try:
            table_element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, self.config['main_element_selector'])))
            headers = [header.text for header in table_element.find_elements(By.CSS_SELECTOR, self.config['header_selector'])]
            rows = table_element.find_elements(By.CSS_SELECTOR, self.config['row_selector'])

            for i in range(min(self.config['num_items'], len(rows))):  # Limitar el número de filas
                row = rows[i]
                cells = row.find_elements(By.CSS_SELECTOR, self.config['cell_selector'])
                row_data = [cell.text for cell in cells]
                table_data.append(row_data)

            table_data.insert(0, headers)
        except Exception as e:
            print(f"Error al extraer información genérica: {e}")

    def scrape_custom_data(self, table_data):
        try:
            rows = self.driver.find_elements(By.CSS_SELECTOR, self.config['row_selector'])
            for i in range(min(self.config['num_items'], len(rows))):
                row = rows[i]
                row_data = {}
                for field, selector in self.config['fields'].items():
                    elements = row.find_elements(By.CSS_SELECTOR, selector)
                    row_data[field] = elements[0].text.strip() if elements else None
                table_data.append(row_data)
        except Exception as e:
            print(f"Error al extraer información personalizada: {e}")

    def create_data(self, data):
        data_dict = data
        try:
            if not isinstance(data[0], dict):
                # Convert data to Dictionary
                data_dict = {data[0][i]: [data[j][i] for j in range(1, len(data))] for i in range(len(data[0]))}
            return data_dict
        except Exception as e:
            print(f"Error al crear el DataFrame: {e}")
    def close_driver(self):
        try:
            self.driver.quit()
        except Exception as e:
            print(f"Error al cerrar el navegador: {e}")