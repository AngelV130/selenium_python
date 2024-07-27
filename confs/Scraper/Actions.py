from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import inspect
from confs.Scraper.Selenium import Selenium

class Actions(Selenium):
    def __init__(self, driver):
        self.driver = driver

    def click(self, selector):
        element = self.element(selector)
        element.click()

    def input(self, selector, value):
        element = self.element(selector)
        element.send_keys(value)

    def select(self, selector, value):
        element = self.element(selector)
        for option in element.find_elements(By.TAG_NAME, 'option'):
            if option.text == value:
                option.click()
                break

    def submit(self, selector):
        element = self.element(selector)
        element.send_keys(Keys.RETURN)

    def hover(self, selector):
        element = self.element(selector)
        ActionChains(self.driver).move_to_element(element).perform()

    def perform_actions(self, actions):
        try:
            for action in actions:
                action_type = action['type']
                action_selector = action['selector']
                if action_type and action_selector:
                    method_name = action_type.replace(' ', '_')
                    method = getattr(self, method_name)
                    num_params = len(inspect.signature(method).parameters)
                    if num_params == 2:
                        value = action.get('value', '')
                        method(action_selector, value)
                    else:
                        method(action_selector)
                else:
                    print(f"Error: {action} no tiene todos los parámetros necesarios.")
        except Exception as e:
            print(f"Error al realizar las acciones: {e}")