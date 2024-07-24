
# Understanding automation
> Since the testing humans actually do cannot be put into words, it cannot be encoded and therefore cannot be automated. We should not use a term that implies it can be.   - James Bach & Michael Bolton from *A Context-Driven Approach to Automation in Testing*

> **Output Checks.** Mechanized or mechanizable processes for gathering product observations and evaluating them. A test is always human-guided, whereas a check, by definition, can be completely automated. A test often includes one or more checks, but a check cannot include a test.   - James Bach, Jonathan Bach & Michael Bolton from *Elements of Excellent Testing*

The two quotes above lay a groundwork for how use of this software should proceed. It is not without the human's intervention that any script here can be utilized. Therefore, what are commonly referred to as "test scripts" will instead be referred to as "check scripts" here.

# Check2U
This software is designed to allow the quick implementation of check scripts. Check scripts can be added to the software and then run with any parameters defined from within the script itself. 

Currently, Check2U can only run python-based scripts written in the [Appium](https://appium.io/docs/en/latest/) framework.

## Example script

```python
import unittest
from appium import webdriver  
from appium.options.android import UiAutomator2Options  
from appium.webdriver.common.appiumby import AppiumBy

definition = dict(
	script_name='Simple Check Script',
	description='And example script for this README.md!',
	parameters=dict(
		element_xpath='//*[@text="Battery"]'
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

class ExampleCheckScript(unittest.TestCase):  
    def setUp(self) -> None:  
        self.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))  
  
    def tearDown(self) -> None:  
        if self.driver:  
            self.driver.quit()  
  
    def test_find_battery(self) -> None:
	    params = definition['parameters']
        el = self.driver.find_element(by=AppiumBy.XPATH, value=params['element_xpath'])  
        el.click()
```

## Creating variable scripts
By default, any class that inherits from the unittest.TestCase class is a runnable script. All check scripts are run as modules from the backend, and may contain a `definition` to make them a variable script. Variable scripts may contain `parameters` and other fields that allow them to use variable data in the script that has been input by the user.

### `definition` module-level variable
The `definition` variable is unsurprisingly used for defining various attributes about the check script. It is a dict object that should be defined at the module-level within your script. A `definition` declaration may look like:
```python
definition = dict(  
	script_name = 'Example Script',
	description = 'An example check script.',
	parameters = dict(
		foo='bar',
		choice=True,
		click_count=3,
	)
)
```
#### `definition` fields
| field | description |
|--|--|
| `script_name` | (Optional) Defines what name should be displayed for the script on the script page. If not defined, app will take the file name and alter it as such: `example_script.py` -> `Example Script` |
| `description` | (Optional) The description to be displayed for the script on the script page. |
| `parameters` | (Optional) A dict object of parameter definitions explained below. |

#### Creating and using parameters
In order to define any form of user input, a script may define `parameters`. Currently, these are just a dictionary of `<key>=<value>` pairs within the `definition` module-level variable. ***Note:** parameters should always be set with a default value that will allow the script to run if no user input is given.*

When passed to the script at execution, the `parameters` field is overwritten with the user input (see `main()` example above). So, all fields of the `parameters` dictionary will now either have the new inputted value, or will have maintain their old default value. This means that a parameter can be accessed in a check script by calling it directly:
```python
definition = dict(
	parameters = dict(
		element_xpath='//*[@text="Battery"]'   # Default value
	)
)
...
# Within ExampleCheckScript class
def check_find_element(self) -> None:
	params = definition['parameters']
	el = self.driver.find_element(by=AppiumBy.XPATH,value=params['element_xpath'])
	el.click()
```

## Future Goals

 - Add more robust input definitions for special input types
	 - Dropdowns
	 - Objects
	 - Files
- Cloud host scripts

