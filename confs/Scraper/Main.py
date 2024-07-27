from confs.Scraper.Selenium import Selenium
from confs.Scraper.Actions import Actions
from confs.Scraper.Scraper import Scraper

class Main:
    def __init__(self, browser_name='Chrome'):
        self.selenium = Selenium(browser_name)
        self.selenium.initialize_driver()
        self.actions = Actions(self.selenium.driver)
        self.scraper = Scraper(self.selenium.driver)

    def create_data(self, data):
        try:
            if not isinstance(data[0], dict):
                data_dict = {data[0][i]: [data[j][i] for j in range(1, len(data))] for i in range(len(data[0]))}
            else:
                data_dict = data
            return data_dict
        except Exception as e:
            print(f"Error al crear el DataFrame: {e}")

    def run(self, config):
        try:
            self.selenium.driver.get(config['url'])
            self.actions.perform_actions(config['actions'])
            data = [] 
            if 'paginate' in config:
                for i in range(config['paginate']['repeat']):
                    data.extend(self.scraper.scrape_data(config['scrape']))
                    self.actions.click(config['paginate']['selector'])
            else:
                data.extend(self.scraper.scrape_data(config['scrape']))
            return self.create_data(data)
        except Exception as e:
            print(f"Error en la ejecución del flujo: {e}")

    def close(self):
        self.selenium.close_driver()