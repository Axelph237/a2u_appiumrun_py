import sys
import time
import unittest
import logging
import json
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

input_parameters = dict(
     input1="value",
     input2=1,
     input3=True
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
        logging.info("Starting test_find_battery")
        self.driver.implicitly_wait(70)

        logging.info("Clicking 'I Understand' button")
        el1 = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="I Understand")
        el1.click()
        time.sleep(1)

        logging.info("Clicking 'I Agree' button")
        el2 = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="I Agree")
        el2.click()
        time.sleep(3)

        for _ in range(7):
            logging.info("Clicking image element")
            el3 = self.driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.Image")
            self.driver.implicitly_wait(3)
            el3.click()
            time.sleep(1)

        logging.info("Clearing and entering API URL")
        el4 = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"https://api.accountable2you.com\")")
        el4.clear()
        time.sleep(1)
        el5 = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.EditText\").instance(0)")
        el5.send_keys("https://api.accountable2you.dev")
        time.sleep(1)

        logging.info("Entering account name")
        el6 = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.EditText\").instance(1)")
        el6.send_keys("appium-javapartner")
        time.sleep(1)

        logging.info("Entering password")
        el7 = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.EditText\").instance(2)")
        el7.send_keys("Appium123!")
        time.sleep(1)

        logging.info("Scrolling to and clicking 'Log In' button")
        el8 = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("Log In"))')
        el8.click()
        time.sleep(5)


# TODO fix error where tests are not liking no input from the front end
# Main will be run by a standard command line execution: 'python foo.py <inputData>'
def main(user_input):
    # explicitly declares inputData declaration as global
    global input_parameters
    if isinstance(user_input, dict):
        input_parameters = user_input
    # run unittest from Appium test class
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPALogin)
    unittest.TextTestRunner(verbosity=2).run(suite)


def get_parameters():
    return input_parameters


if __name__ == '__main__':
    main(None)
