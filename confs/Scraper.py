from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time

class Scraper:
    def __init__(self, config):
        self.config = config
        self.options = Options()
        self.options.headless = False
        self.options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.options)

    def navigate_to_page(self):
        try:
            self.driver.get(self.config['url'])
            data = [self.perform_actions()]
            if 'paginate' in self.config:
                self.config['actions'] = [{'type': 'click', 'selector': self.config['paginate']['selector']}]
                for i in range(self.config['paginate']['repeat']):
                    data.append(self.perform_actions())
                return data
            else:
                return data
        except Exception as e:
            print(f"Error al cargar la página: {e}")

    def perform_actions(self):
        try:
            if 'actions' in self.config:
                for action in self.config['actions']:
                    element = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, action['selector'])))
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
                    elif action['type'] == 'hover':
                        # Realizar hover sobre el elemento
                        ActionChains(self.driver).move_to_element(element).perform()
            return self.scrape_data()
        except Exception as e:
            print(f"Error al realizar las acciones: {e}")

    def scrape_data(self):
        try:
            time.sleep(3)
            table_data = []
            if 'fields' in self.config:
                self.scrape_custom_data(table_data)
            else:
                self.scrape_generic_data(table_data)
            return self.create_data(table_data)
        except Exception as e:
            print(f"Error al extraer la información: {e}")

    def scrape_generic_data(self, data_list):
        try:
            main_element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.config['main_element_selector']))
            )
            headers = []
            if 'header_selector' in self.config:
                headers = [header.text for header in main_element.find_elements(By.CSS_SELECTOR, self.config['header_selector'])]
                data_list.append(headers)

            rows = main_element.find_elements(By.CSS_SELECTOR, self.config['row_selector'])

            for i in range(min(self.config.get('num_items', len(rows)), len(rows))):
                row = rows[i]
                cells = row.find_elements(By.CSS_SELECTOR, self.config['cell_selector'])
                row_data = [cell.text for cell in cells]
                data_list.append(row_data)
        except Exception as e:
            print(f"Error al extraer los datos: {e}")

    def scrape_custom_data(self, table_data):
        try:
            main_element = self.driver
            if 'main_element_selector' in self.config:
                main_element = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, self.config['main_element_selector']))
                )
            rows = main_element.find_elements(By.CSS_SELECTOR, self.config['row_selector'])
            
            for i in range(min(self.config.get('num_items', len(rows)), len(rows))):
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
                data_dict = {data[0][i]: [data[j][i] for j in range(1, len(data))] for i in range(len(data[0]))}
            return data_dict
        except Exception as e:
            print(f"Error al crear el DataFrame: {e}")
    def close_driver(self):
        try:
            self.driver.quit()
        except Exception as e:
            print(f"Error al cerrar el navegador: {e}")