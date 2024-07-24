import sys
import time
import unittest
import logging
import json
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

definition = dict(
    script_name='Reports App Login',
    description='A simple tool for checking the login functionality of the Reports App.',
    parameters=dict(
        top_level_domain='com',
        username='none',
        password='none',
    )
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("appium_test.log"),
        logging.StreamHandler()
    ]
)


capabilities = dict(
    platformName='Android',
    deviceName='emulator-5554',
    automationName='uiautomator2',
    appPackage='com.accountable2you.reportsapp',
    appActivity='com.accountable2you.reportsapp.MainActivity'
)

appium_server_url = 'http://localhost:4723'


class TestPALogin(unittest.TestCase):
    def setUp(self) -> None:
        logging.info("Initializing Appium driver")
        self.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))
        logging.info("Appium driver initialized")

    def tearDown(self) -> None:
        if self.driver:
            logging.info("Quitting Appium driver")
            self.driver.quit()
            logging.info("Appium driver quit")

    def test_login(self) -> None:
        global definition
        print("INPUTS FROM TEST_PA_LOGIN.TestPALogin.test_login: " + str(input_parameters))

        self.driver.implicitly_wait(70)
        logging.info("Clicking 'I Understand' button")
        self.driver.switch_to.context("WEBVIEW_com.accountable2you.reportsapp")
        time.sleep(5)
        el1 = self.driver.find_element(by=AppiumBy.XPATH, value="//a[@id=\"btnConfirmReports\"]")
        el1.click()
        time.sleep(1)

        logging.info("Clicking 'I Agree' button")
        el2 = self.driver.find_element(by=AppiumBy.XPATH, value="//app-terms/ion-content/div/div/a")
        el2.click()
        time.sleep(3)

        for _ in range(7):
            logging.info("Clicking image element")
            el3 = self.driver.find_element(by=AppiumBy.XPATH, value="(//img[@id=\"a2uLogo\"])[3]")
            self.driver.implicitly_wait(3)
            el3.click()
            time.sleep(1)

        logging.info("Clearing and entering API URL")
        el4 = self.driver.find_element(by=AppiumBy.XPATH, value="//input[@name=\"baseUrl\"]")
        el4.clear()
        el4.send_keys("https://api.accountable2you.dev")
        time.sleep(1)

        logging.info("Entering account name")
        el5 = self.driver.find_element(by=AppiumBy.XPATH, value="//input[@name=\"acctName\"]")
        el5.send_keys("appium-javapartner")
        time.sleep(1)

        logging.info("Entering password")
        el6 = self.driver.find_element(by=AppiumBy.XPATH, value="//input[@name=\"pswd\"]")
        el6.send_keys("Appium123!")
        time.sleep(1)

        logging.info("Scrolling to and clicking 'Log In' button")
        el7 = self.driver.find_element(by=AppiumBy.XPATH, value="//a[@id=\"btnLogIn\"]")
        el7.click()

        time.sleep(5)
        el8 = self.driver.find_element(AppiumBy.XPATH, "//app-filter-menu-bar/div/label[3]")
        el8.click()

        time.sleep(5)


def main():
    # run unittest from Appium test class
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPALogin)
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    main()
