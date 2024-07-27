from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Selenium:
    def __init__(self, browser_name='Chrome'):
        self.browser_name = browser_name
        self.options = self.initialize_options()
        self.driver = None

    def initialize_options(self):
        if self.browser_name == 'Chrome':
            options = ChromeOptions()
            options.headless = True
            options.add_argument('--start-maximized')
            return options
        elif self.browser_name == 'Firefox':
            options = FirefoxOptions()
            options.headless = True
            return options
        elif self.browser_name == 'Edge':
            options = EdgeOptions()
            options.headless = True
            return options
        else:
            raise ValueError("Browser not supported.")

    def initialize_driver(self):
        if self.browser_name == 'Chrome':
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.options)
        elif self.browser_name == 'Firefox':
            self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=self.options)
        elif self.browser_name == 'Edge':
            self.driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=self.options)
        else:
            raise ValueError("Driver not supported.")
    
    def close_driver(self):
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
        except Exception as e:
            print(f"Error al cerrar el navegador: {e}")

    def element(self, selector):
        return WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))