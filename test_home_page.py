import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PAGE_URL = "https://www.trivago.co.uk/"
TIME_TO_WAIT = 5


class TestHomePage(unittest.TestCase):

    def setUp(self):
        self._chrome_options = webdriver.ChromeOptions()
        self._chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(chrome_options=self._chrome_options,
                                       service_args=['--verbose'])

    def test_page_load(self):
        print("When user goes to main page, page should be loaded")
        self.driver.get(PAGE_URL)
        search_input = WebDriverWait(self.driver, TIME_TO_WAIT).until(
            EC.presence_of_element_located((By.ID, 'querytext')))
        self.assertTrue(search_input.is_displayed())

    def test_search_form(self):
        print("When user search hotels in Amsterdam, results should be in Amsterdam")
        self.driver.get(PAGE_URL)
        search_input = WebDriverWait(self.driver, TIME_TO_WAIT).until(
            EC.presence_of_element_located((By.ID, 'querytext')))
        search_input.send_keys("Amsterdam")
        self.driver.find_element(By.XPATH, "//button[@data-qa='search-button']").click()
        info_slideouts = WebDriverWait(self.driver, TIME_TO_WAIT).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@data-qa='info-slideout']")))
        self.assertTrue(len(info_slideouts) > 0)
        for el in info_slideouts:
            self.assertTrue("Amsterdam" in el.text)

    def test_login(self):
        print("User should be able to log in")
        self.driver.get(PAGE_URL)
        WebDriverWait(self.driver, TIME_TO_WAIT).until(
            EC.presence_of_element_located((By.XPATH, "//button[@data-qa='header-login']"))).click()
        self.driver.find_element(By.ID, "check_email").send_keys("werewr@mailinator.com")
        WebDriverWait(self.driver, TIME_TO_WAIT).until(
            EC.presence_of_element_located((By.ID, "login_email_submit"))).click()
        WebDriverWait(self.driver, TIME_TO_WAIT).until(
            EC.visibility_of_element_located((By.ID, "login_password"))).send_keys("password")
        self.driver.find_element(By.ID, "login_submit").click()
        user_email = WebDriverWait(self.driver, TIME_TO_WAIT).until(
            EC.presence_of_element_located((By.ID, "user-text"))).text
        self.assertEqual(user_email, "werewr@mailinator.com")

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestHomePage)
    unittest.TextTestRunner(verbosity=2).run(suite)
