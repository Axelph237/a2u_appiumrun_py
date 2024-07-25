import sys
import unittest
import json
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

definition = dict(
    script_name='Multi Params Example',
    description='An example description.',
    parameters=dict(
        string_input='Hello world!',
        number_input=10,
        bool_input=True,
    )
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

    def test_print(self) -> None:
        params = definition['parameters']
        print('Test begun successfully with following parameters:')
        print(f'string_input: {params["string_input"]}')
        print(f'number_input: {params["number_input"]}')
        print(f'bool_input: {params["bool_input"]}')

