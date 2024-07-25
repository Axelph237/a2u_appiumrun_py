import sys
import unittest
import json
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

definition = dict(
    script_name='Example Test',
    description='An example description.',
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


class PseudoCheck(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def check_print(self) -> None:
        print('Test run successfully.')
