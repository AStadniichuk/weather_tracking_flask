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

    def test_aa_generate_database(self):
        self.browser.get(self.base_url)
        self.assertEqual(self.browser.title, 'Home page')
        generate_db_link = self.browser.find_element(By.ID, 'submit')
        generate_db_link.click()
        alert_text = self.browser.find_element(By.ID, 'alert_block').text
        self.assertIn('Database filled with test data', alert_text)

    def test_ab_login_with_new_credentials(self):
        with open(PATH_TO_CREDENTIALS) as file:
            credentials = json.load(file)

        type(self).random_user = random.choice(credentials)
        self.browser.find_element(By.ID, 'loginLink').click()
        self.assertEqual(self.browser.title, 'Login')

        self.browser.find_element(By.ID, 'email').send_keys(self.random_user['email'])
        self.browser.find_element(By.ID, 'password').send_keys(self.random_user['password'])
        self.browser.find_element(By.ID, 'submit').click()

        hello_message = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn(f'Hello, {self.random_user["username"]}', hello_message)
        self.assertEqual(self.browser.current_url, self.base_url)

    def test_ac_logout_user(self):
        self.browser.find_element(By.ID, 'logoutLink').click()
        alert_text = self.browser.find_element(By.ID, 'alert_block').text
        self.assertIn('You have been logged out', alert_text)
