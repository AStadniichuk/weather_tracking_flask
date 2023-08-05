import json
import unittest
import random
from selenium import webdriver
from selenium.webdriver.common.by import By

from definitions import PATH_TO_CREDENTIALS


class TestGenerateDB(unittest.TestCase):
    browser: webdriver.chrome = None
    base_url: str = None
    random_user: dict[str, str] = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.browser = webdriver.Chrome()
        cls.base_url = 'http://127.0.0.1:5000/'

    @classmethod
    def tearDownClass(cls) -> None:
        cls.browser.close()
        cls.browser.quit()

    def test_1_show_users_no_login_user(self):
        self.browser.get(self.base_url)

        self.browser.find_element(By.ID, 'users').click()
        self.browser.find_element(By.ID, 'showUsersLink').click()
        alert_message = self.browser.find_element(By.ID, 'alert_block').text
        self.assertIn('Please log in to access this page.', alert_message)

    def test_2_show_users_no_admin(self):
        with open(PATH_TO_CREDENTIALS) as file:
            credentials = json.load(file)

        users = [user for user in credentials if user['role'] == 'user']
        type(self).random_user = random.choice(users)
        self.browser.find_element(By.ID, 'loginLink').click()
        self.assertEqual(self.browser.title, 'Login')

        self.browser.find_element(By.ID, 'email').send_keys(self.random_user['email'])
        self.browser.find_element(By.ID, 'password').send_keys(self.random_user['password'])
        self.browser.find_element(By.ID, 'submit').click()

        for test in range(2):
            self.browser.find_element(By.ID, 'users').click()
            self.browser.find_element(By.ID, 'showUsersLink').click()
            if test == 0:
                self.browser.find_element(By.ID, 'editLink').click()
                forbidden_message = self.browser.find_element(By.TAG_NAME, 'h1').text
                self.assertIn(
                    "403 Forbidden: You don't have the permission to access the requested resource. It is either read-protected or not readable by the server",
                    forbidden_message)
            else:
                self.browser.find_element(By.ID, 'selectButton').click()
                self.browser.find_element(By.ID, 'deleteButton').click()
                alert_message = self.browser.find_element(By.ID, 'alert_block').text
                self.assertIn("You don't have access to delete users", alert_message)
        self.browser.find_element(By.ID, 'logoutLink').click()

    def test_3_show_users_admin(self):
        with open(PATH_TO_CREDENTIALS) as file:
            credentials = json.load(file)

        admin_users = [user for user in credentials if user['role'] == 'admin']
        id_users = [user['id'] for user in credentials if user['role'] == 'user']
        id_user = random.choice(id_users)
        for user in credentials:
            if user['id'] == id_user:
                email_user = user['email']

        type(self).random_user = random.choice(admin_users)
        self.browser.find_element(By.ID, 'loginLink').click()
        self.assertEqual(self.browser.title, 'Login')

        self.browser.find_element(By.ID, 'email').send_keys(self.random_user['email'])
        self.browser.find_element(By.ID, 'password').send_keys(self.random_user['password'])
        self.browser.find_element(By.ID, 'submit').click()

        self.browser.find_element(By.ID, 'users').click()
        self.browser.find_element(By.ID, 'showUsersLink').click()
        self.browser.find_element(By.ID, 'deleteButton').click()
        alert_message = self.browser.find_element(By.ID, 'alert_block').text
        self.assertIn('Nothing to delete', alert_message)

        self.browser.find_element(By.XPATH,
                                  f'/html/body/div[2]/form/div/table/tbody/tr[{self.random_user["id"]}]/td[1]/input').click()
        self.browser.find_element(By.ID, 'deleteButton').click()
        alert_message = self.browser.find_element(By.ID, "alert_block").text
        self.assertIn("You can't delete yourself use profile page for this", alert_message)

        self.browser.find_element(By.ID, 'editLink').click()
        self.browser.find_element(By.ID, 'username').clear()
        self.browser.find_element(By.ID, 'username').send_keys('jack')
        self.browser.find_element(By.ID, 'submit').click()
        alert_message = self.browser.find_element(By.ID, 'alert_block').text
        self.assertIn(f'jack updated', alert_message)

        self.browser.find_element(By.XPATH,
                                  f'/html/body/div[2]/form/div/table/tbody/tr[{id_user}]/td[1]/input').click()
        self.browser.find_element(By.ID, 'deleteButton').click()
        alert_message = self.browser.find_element(By.ID, 'alert_block').text
        self.assertIn(f'Deleted: {email_user}', alert_message)
