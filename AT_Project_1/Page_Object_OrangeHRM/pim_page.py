from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import random
import string
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

logger = logging.getLogger(__name__)


class PIMPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)  # Initialize WebDriverWait
        self.generated_id = None

        self.username_input = (By.XPATH, '//*[@id="app"]/div[1]/div/div[1]/div/div[2]/div[2]/form/div[1]/div/div[2]/input')
        self.password_input = (By.XPATH, '//*[@id="app"]/div[1]/div/div[1]/div/div[2]/div[2]/form/div[2]/div/div[2]/input')
        self.login_button = (By.CSS_SELECTOR,"#app > div.orangehrm-login-layout > div > div.orangehrm-login-container > div > div.orangehrm-login-slot > div.orangehrm-login-form > form > div.oxd-form-actions.orangehrm-login-action > button")

        self.pim_module = (By.XPATH, '//*[@id="app"]/div[1]/div[1]/aside/nav/div[2]/ul/li[2]/a')

        self.add_employee = (By.XPATH, '//*[@id="app"]/div[1]/div[1]/header/div[2]/nav/ul/li[3]/a')
        self.employee_name = (By.XPATH,'//*[@id="app"]/div[1]/div[2]/div[2]/div/div/form/div[1]/div[2]/div[1]/div[1]/div/div/div[2]/div[1]/div[2]/input')
        self.employee_lastname = (By.XPATH,'//*[@id="app"]/div[1]/div[2]/div[2]/div/div/form/div[1]/div[2]/div[1]/div[1]/div/div/div[2]/div[3]/div[2]/input')
        self.employee_id = (By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/form/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/input')
        self.save_button = (By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/form/div[2]/button[2]')

        self.emloyee_id_sreach_feild = (By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div[1]/div[2]/form/div[1]/div/div[2]/div/div[2]/input')
        self.emloyee_id_sreach_button = (By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div[1]/div[2]/form/div[2]/button[2]')
        self.edit_button = (By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div[2]/div[3]/div/div[2]/div[1]/div/div[9]/div/button[2]/i')
        self.driver_license_feild = (By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/div/div[2]/div[1]/form/div[2]/div[2]/div[1]/div/div[2]/input')
        self.save_button_in_edit_inforamtion = (By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/div/div[2]/div[1]/form/div[4]/button')
        self.success_message_in_edit_information = (By.XPATH, '// *[ @ id = "oxd-toaster_1"] / div')


        self.delete_button = (By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div[2]/div[3]/div/div[2]/div[1]/div/div[9]/div/button[1]')

        self.confirm_delete_button = (By.XPATH, '//*[@id="app"]/div[3]/div/div/div/div[3]/button[2]')


        self.success_message_locator = (By.XPATH, '//*[@id="oxd-toaster_1"]/div')


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


    def go_to_pim_module(self):

        click_pim_module = self.wait.until(EC.element_to_be_clickable(self.pim_module))
        self.driver.implicitly_wait(10)
        click_pim_module.click()
        self.driver.implicitly_wait(10)


    def add_new_employee(self, firstname , lastname):
        # Wait for the 'Add Employee' button to be clickable
        add_employee_button = self.wait.until(EC.element_to_be_clickable(self.add_employee))
        add_employee_button.click()
        self.driver.implicitly_wait(10)

        # Wait for the employee name input field and enter Firstname
        employee_name_field = self.wait.until(EC.visibility_of_element_located(self.employee_name))
        employee_name_field.send_keys(firstname )
        self.driver.implicitly_wait(10)

        # Wait for the employee lastname input field and enter Lastname
        employee_lastname_field = self.wait.until(EC.visibility_of_element_located(self.employee_lastname))
        employee_lastname_field.send_keys(lastname)
        self.driver.implicitly_wait(15)

        upper_letter = random.choice(string.ascii_uppercase)
        lower_letter = random.choice(string.ascii_lowercase)
        digits = ''.join(random.choice(string.digits) for _ in range(2))
        self.generated_id = upper_letter + lower_letter + digits


        # Wait for the employee Id input field and enter Lastname
        employee_id_field = self.wait.until(EC.visibility_of_element_located(self.employee_id))
        employee_id_field.send_keys(self.generated_id)
        self.driver.implicitly_wait(15)


        # Wait for the save button to be clickable and click it
        save_button = self.wait.until(EC.element_to_be_clickable(self.save_button))
        save_button.click()
        self.driver.implicitly_wait(10)

    def validate_success_message(self):
        # Wait for the success message element to be visible
        success_message = self.wait.until(EC.visibility_of_element_located(self.success_message_locator))
        print(success_message.text)
        # Validate the success message text
        if "Successfully Saved" in success_message.text:
            print("Employee added successfully.")
        else:
            print("Failed to add employee. Unexpected success message.")

    def search_employee(self):
        if self.generated_id is None:
            print("No employee ID generated yet.")
            return

        print(f"Searching for ID: {self.generated_id}")

        emloyee_id_feild  = self.wait.until(EC.element_to_be_clickable(self.emloyee_id_sreach_feild))
        emloyee_id_feild.send_keys(self.generated_id)
        self.driver.implicitly_wait(10)

        sreach_button = self.wait.until(EC.element_to_be_clickable(self.emloyee_id_sreach_button))
        sreach_button.click()
        self.driver.implicitly_wait(10)

        # self.driver.find_element(self.emloyee_id_sreach_feild).send_keys(id)
        # self.driver.find_element(self.emloyee_id_sreach_button).click()

    def edit_employee(self):
        click_edit_button= WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(self.edit_button))
        self.driver.execute_script("arguments[0].click();",click_edit_button)
        self.driver.implicitly_wait(15)

        # Wait for the driving linces input field to be visible
        license_feild = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(self.driver_license_feild))
        license_feild.send_keys("0001")
        self.driver.implicitly_wait(10)

        save_button  = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(self.save_button_in_edit_inforamtion))
        self.driver.execute_script("arguments[0].click();", save_button)
        #save_button.click()
        self.driver.implicitly_wait(15)

        # save_button = self.wait.until(EC.element_to_be_clickable(self.save_button_in_edit_inforamtion ))
        # save_button.click()
        # self.driver.implicitly_wait(10)











    def delete_employee(self):
        element_expand = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(self.delete_button))
        self.driver.execute_script("arguments[0].click();", element_expand)
        self.driver.implicitly_wait(15)
        # # Wait for the delete button to be visible and scroll into view
        # delete_button_element = self.wait.until(EC.visibility_of_element_located(self.delete_button))
        # self.driver.execute_script("arguments[0].scrollIntoView();", delete_button_element)
        delete_button_element = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(self.confirm_delete_button))
        self.driver.execute_script("arguments[0].click();", delete_button_element)
        self.driver.implicitly_wait(15)

        # # Ensure the delete button is clickable
        # delete_button_element = self.wait.until(EC.element_to_be_clickable(self.delete_button))
        #
        # # Click the delete button
        # try:
        #     delete_button_element.click()
        # except ElementClickInterceptedException:
        #     # Use JavaScript click if normal click fails
        #     self.driver.execute_script("arguments[0].click();", delete_button_element)



        # # Optionally, wait for a success message or another element that indicates the deletion was successful
        # success_message = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="oxd-toaster_1"]/div')))
        # print(success_message.text)
        # if "Successfully Deleted" in success_message.text:
        #     print("Employee deleted successfully.")
        # else:
        #     print("Failed to delete employee. Unexpected success message.")



    def get_success_message(self):
        return self.driver.find_element(*self.success_message).text
