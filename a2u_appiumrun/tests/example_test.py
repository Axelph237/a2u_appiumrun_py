import sys
import unittest
import json
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

input_parameters = dict(
    input1=False,
    input2=1,
    input3=True,
    input4="Hello World",
    example_input="value",
)

capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='emulator-5554',
    appPackage='com.android.settings',
    appActivity='.Settings',
    ensureWebviewsHavePages='true',
    nativeWebScreenshot='true',
    newCommandTimeout=3600,
    connectHardwareKeyboard='true',
    language='en',
    locale='US'
)

appium_server_url = 'http://localhost:4723'


class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def test_find_battery(self) -> None:
        el = self.driver.find_element(by=AppiumBy.XPATH, value='//*[@text="Battery"]')
        el.click()


# Main will be run by a standard command line execution: 'python foo.py <inputData>'
def main(user_input):
    # explicitly declares inputData declaration as global
    global input_parameters
    if isinstance(user_input, dict):
        input_parameters = user_input
    # run unittest from Appium test class
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAppium)
    unittest.TextTestRunner(verbosity=2).run(suite)


def get_parameters():
    return input_parameters


if __name__ == '__main__':
    main(None)
