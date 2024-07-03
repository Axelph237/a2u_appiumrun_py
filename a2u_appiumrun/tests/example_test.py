import sys
import unittest
import json
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

inputData = dict(
    input1="value",
    input2=1,
    input3=True
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
def main():
    # explicitly declares inputData declaration as global
    global inputData
    print(sys.argv[1])
    inputData = json.loads(sys.argv[1])
    unittest.main(argv=[sys.argv[0]])


# Read_Requirements passes the script's required input along the command line to the server backend
# It is run when the script is executed with the '-r' argument: 'python foo.py -r'
def read_requirements():
    print(inputData)


# This will be the entry point of the file when run from the command line
if __name__ == '__main__':
    if sys.argv[1] == '-r':
        read_requirements()
    else:
        main()
