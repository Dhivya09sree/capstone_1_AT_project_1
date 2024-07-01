from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

logger = logging.getLogger(__name__)

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.username_input = (By.XPATH, '//*[@id="app"]/div[1]/div/div[1]/div/div[2]/div[2]/form/div[1]/div/div[2]/input')
        self.password_input = (By.XPATH, '//*[@id="app"]/div[1]/div/div[1]/div/div[2]/div[2]/form/div[2]/div/div[2]/input')
        self.login_button = (By.CSS_SELECTOR, "#app > div.orangehrm-login-layout > div > div.orangehrm-login-container > div > div.orangehrm-login-slot > div.orangehrm-login-form > form > div.oxd-form-actions.orangehrm-login-action > button")
        self.error_message = (By.CSS_SELECTOR, "#app > div.orangehrm-login-layout > div > div.orangehrm-login-container > div > div.orangehrm-login-slot > div.orangehrm-login-form > div > div.oxd-alert.oxd-alert--error > div.oxd-alert-content.oxd-alert-content--error > p")

    def login(self, username, password):

        username_element = self.wait.until(EC.presence_of_element_located(self.username_input))
        username_element.send_keys(username)
        logger.info("Enter the username"+username)


        password_element = self.wait.until(EC.presence_of_element_located(self.password_input))
        password_element.send_keys(password)
        logger.info("Enter Password"+password)


        login_button_element = self.wait.until(EC.element_to_be_clickable(self.login_button))
        login_button_element.click()
        logger.info("Login button clicked")

    def get_error_message(self):
        logger.info("Attempting to retrieve error message")
        error_message_element = self.wait.until(EC.presence_of_element_located(self.error_message))
        error_message = error_message_element.text
        logger.info(f"Error message retrieved: {error_message}")
        return error_message
