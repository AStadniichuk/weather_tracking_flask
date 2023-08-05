import json
import unittest
import random

from selenium import webdriver
from selenium.webdriver.common.by import By

from definitions import PATH_TO_CREDENTIALS


class TestWeather(unittest.TestCase):
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

    def test_1_weather_info_no_user(self):
        self.browser.get(self.base_url)

        self.browser.find_element(By.ID, 'weather').click()
        self.browser.find_element(By.ID, 'weatherInfoLink').click()

        self.browser.find_element(By.ID, 'city_name').send_keys('tokyo')
        self.browser.find_element(By.ID, 'submit').click()
        self.browser.find_element(By.ID, 'addCity').click()
        alert_message = self.browser.find_element(By.ID, 'alert_block').text
        self.assertIn('Please log in to access this page.', alert_message)

    def test_2_weather_monitor_no_user(self):
        self.browser.find_element(By.ID, 'weather').click()
        self.browser.find_element(By.ID, 'weatherMonitorLink').click()

        alert_message = self.browser.find_element(By.ID, 'alert_block').text
        self.assertIn('Please log in to access this page.', alert_message)

    def test_3_weather_info(self):
        with open(PATH_TO_CREDENTIALS) as file:
            credentials = json.load(file)

        type(self).random_user = random.choice(credentials)
        self.browser.find_element(By.ID, 'loginLink').click()
        self.assertEqual(self.browser.title, 'Login')

        self.browser.find_element(By.ID, 'email').send_keys(self.random_user['email'])
        self.browser.find_element(By.ID, 'password').send_keys(self.random_user['password'])
        self.browser.find_element(By.ID, 'submit').click()

        self.browser.find_element(By.ID, 'weather').click()
        self.browser.find_element(By.ID, 'weatherInfoLink').click()

        for total in range(2):
            self.browser.find_element(By.ID, 'city_name').send_keys('london')
            self.browser.find_element(By.ID, 'submit').click()
            self.browser.find_element(By.ID, 'addCity').click()

            city_added_message = self.browser.find_element(By.ID, 'alert_block').text
            self.assertIn(
                f'City London added to user {self.random_user["username"]}'
                if total == 0 else
                f'City London already in list of user {self.random_user["username"]}',
                city_added_message)
        self.browser.find_element(By.ID, 'logoutLink').click()

    def test_4_weather_monitor(self):

        with open(PATH_TO_CREDENTIALS) as file:
            credentials = json.load(file)

        type(self).random_user = random.choice(credentials)
        self.browser.find_element(By.ID, 'loginLink').click()
        self.assertEqual(self.browser.title, 'Login')

        self.browser.find_element(By.ID, 'email').send_keys(self.random_user['email'])
        self.browser.find_element(By.ID, 'password').send_keys(self.random_user['password'])
        self.browser.find_element(By.ID, 'submit').click()

        self.browser.find_element(By.ID, 'weather').click()
        self.browser.find_element(By.ID, 'weatherMonitorLink').click()
        self.browser.find_element(By.ID, 'deleteButton').click()
        alert_message = self.browser.find_element(By.ID, 'alert_block').text
        self.assertIn('Nothing to delete', alert_message)

    def test_5_weather_monitor_with_cities(self):
        cities = ['london', 'paris', 'tokio', 'kyoto']
        id_cities = list(range(1, len(cities) + 1))
        id_city = random.choice(id_cities)

        self.browser.find_element(By.ID, 'weather').click()
        self.browser.find_element(By.ID, 'weatherInfoLink').click()
        for city in cities:
            self.browser.find_element(By.ID, 'city_name').send_keys(city)
            self.browser.find_element(By.ID, 'submit').click()
            self.browser.find_element(By.ID, 'addCity').click()

        self.browser.find_element(By.ID, 'weather').click()
        self.browser.find_element(By.ID, 'weatherMonitorLink').click()
        self.browser.find_element(By.XPATH, f'/html/body/div[2]/form/div/table/tbody/tr[{id_city}]/td[1]/input').click()
        self.browser.find_element(By.ID, 'deleteButton').click()
        alert_message = self.browser.find_element(By.ID, 'alert_block').text
        self.assertIn(f'Delete: {cities[id_city - 1].title()}', alert_message)
