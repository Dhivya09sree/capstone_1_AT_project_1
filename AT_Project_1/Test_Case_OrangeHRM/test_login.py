import logging
import pytest
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from Page_Object_OrangeHRM.Login_page import LoginPage
from utils.excel_utils import get_data
from selenium.common.exceptions import TimeoutException
from Page_Object_OrangeHRM.pim_page import PIMPage


# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('test_login.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class TestLoginPage:
    BASE_URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    EXCEL_FILE_PATH = os.path.abspath("C://Users//dhivy//PycharmProjects//AT_Project_1//data//test_credentials.xlsx")
    EXCEL_SHEET_NAME_LOGIN_VALID = "login"
    EXCEL_SHEET_NAME_LOGIN_INVALID = "login_invalid"

    @pytest.fixture
    def setup(self):
        logger.info("Setting up WebDriver instance")
        driver = webdriver.Chrome()  # or any other WebDriver instance
        yield driver
        logger.info("Tearing down WebDriver instance")
        driver.quit()

    #TC_Login_01
    @pytest.mark.parametrize("row, Username, Password", [(idx, *data) for idx, data in
                                                         enumerate(get_data(EXCEL_FILE_PATH, EXCEL_SHEET_NAME_LOGIN_VALID), start=2)])
    def test_login(self, setup, row, Username, Password):
        logger.info("TC_Login_01")

        logger.info(f"Starting test case for row {row} with Username: {Username} and Password: {Password}")
        self.driver = setup
        self.driver.get(self.BASE_URL)
        logger.info(f"Navigated to {self.BASE_URL}")

        login_page = LoginPage(self.driver)
        login_page.login(Username, Password)
        logger.info(f"Attempted login with Username: {Username} and Password: {Password}")

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/header/div[1]/div[1]/span/h6')))
            logger.info("Login successful, no error message retrieved.")
        except TimeoutException:
            actual_error = login_page.get_error_message()
            logger.error(f"Login failed, retrieved error message: {actual_error}")
            # Capture screenshot upon test failure
            self.capture_screenshot(row)
            raise

    #TC_Login_02
    @pytest.mark.parametrize("row, Username, Password", [(idx, *data) for idx, data in
                                                         enumerate(get_data(EXCEL_FILE_PATH, EXCEL_SHEET_NAME_LOGIN_INVALID), start=2)])
    def test_login_invalid(self, setup, row, Username, Password):
        logger.info("TC_Login_02")

        logger.info(f"Starting invalid login test case for row {row} with Username: {Username} and Password: {Password}")
        self.driver = setup
        self.driver.get(self.BASE_URL)
        logger.info(f"Navigated to {self.BASE_URL}")

        login_page = LoginPage(self.driver)
        login_page.login(Username, Password)
        logger.info(f"Attempted login with Username: {Username} and Password: {Password}")

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/header/div[1]/div[1]/span/h6')))
            logger.info("Login successful, no error message retrieved.")
        except TimeoutException:
            actual_error = login_page.get_error_message()
            logger.info(f"Login failed as expected, retrieved error message: {actual_error}")
            assert actual_error == "Invalid credentials", f"Unexpected error message: {actual_error}"
            # Capture screenshot upon test failure
            self.capture_screenshot(row)

   #TC_PIM_01
    def test_Add_Employee(self, setup):

        logger.info("TC_PIM_01")
        self.driver = setup
        self.driver.get(self.BASE_URL)
        logger.info(f"Navigated to {self.BASE_URL}")

        pim = PIMPage(self.driver)

        pim.login("Admin","admin123")

        pim.go_to_pim_module()
        logger.info("Clicked the PIM module")

        pim.add_new_employee("Dhivya","k")
        logger.info("Added the new employee in orangeHRM")

        # Wait for the success message element to be visible
        success_message = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="oxd-toaster_1"]/div')))
        print(success_message.text)


        # Validate the success message text
        if "Successfully Saved" in success_message.text:
            print("Employee added successfully.")
            logger.info(f"Employee added successfully: {success_message.text}")

        else:
            print("Failed to add employee. Unexpected success message.")
            logger.error("Failed to add employee. Unexpected success message.")

    def test_edit_employee(self,setup):

        logger.info("TC_PIM_02")
        self.driver = setup
        self.driver.get(self.BASE_URL)
        logger.info(f"Navigated to {self.BASE_URL}")
        self.driver.maximize_window()

        pim = PIMPage(self.driver)

        pim.login("Admin", "admin123")

        pim.go_to_pim_module()
        logger.info("Clicked the PIM module")

        pim.search_employee()
        logger.info("sreach the employee Id")

        pim.edit_employee()
        logger.info("edit the persol information in exit employee ")

        # Wait for the success message element to be visible
        success_message = WebDriverWait(self.driver, 10).until( EC.presence_of_element_located((By.XPATH, '// *[ @ id = "oxd-toaster_1"] / div')))
        print(success_message.text)

        # Validate the success message text
        if "Successfully Updated" in success_message.text:
            print("Employee Updated  successfully.")
            logger.info(f"Employee Updated  successfully: {success_message.text}")

        else:
            print("Failed to update employee. Unexpected success message.")
            logger.error("Failed to update employee. Unexpected success message.")


    def test_delete_employee(self,setup):
        logger.info("TC_PIM_03")
        self.driver = setup
        self.driver.get(self.BASE_URL)
        logger.info(f"Navigated to {self.BASE_URL}")
        self.driver.maximize_window()

        pim = PIMPage(self.driver)

        pim.login("Admin", "admin123")

        pim.go_to_pim_module()
        logger.info("Clicked the PIM module")

        pim.delete_employee()
        logger.info("deledt the exit the employee")

        # Optionally, wait for a success message or another element that indicates the deletion was successful
        delete_message = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="oxd-toaster_1"]/div/div[1]/div[2]')))
        print(delete_message.text)
        if "Successfully Deleted" in delete_message.text:
            print("Employee deleted successfully.")
            logger.info(f"Employee deleted successfully.: {delete_message.text}")
        else:
            print("Failed to delete employee. Unexpected success message.")
            logger.error("Failed to delete employee.. Unexpected success message.")




    def capture_screenshot(self, test_row):
        screenshot_dir = "screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, f"test_row_{test_row}.png")
        self.driver.save_screenshot(screenshot_path)
        logger.error(f"Screenshot saved for test row {test_row}: {screenshot_path}")
