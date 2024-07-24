import os
import importlib

tests_directory = None
modules = []
definitions = []
initialized = False

# TODO Refactor test_handler to script_handler, including references in views.py
# Used to initialize the module's values
# Arguments:
#   directory: the path to import test modules from
def init(directory):
    global tests_directory, initialized

    try:
        initialized = True
        tests_directory = directory
        load_tests()
    except Exception as e:
        initialized = False
        print('Test Handler initialization failed with exception: ' + str(e))


# Loads all test modules found in the tests_directory
def load_tests():
    global modules, definitions

    if not initialized:
        raise ValueError(f"tests_directory {tests_directory} is None. Module has not been initialized.")

    # Ensuring empty arrays
    definitions.clear()
    modules.clear()

    modules = import_modules(tests_directory, 'a2u_appiumrun.tests')
    create_definitions()


# Imports python modules from the specified directory, given the package name
# Arguments:
#   directory: the path location of the modules
#   package_name: the relative package name, i.e. 'foo.bar'
def import_modules(directory, package_name):
    global modules

    modules = []

    for filename in os.listdir(directory):
        if filename.endswith('.py') and filename != '__init__.py':
            # Remove suffix and create path
            module_name = filename[:-3]
            module_path = f'{package_name}.{module_name}'
            # Import script as a module
            module = importlib.import_module(module_path)
            modules.append(module)

    return modules


# Takes all imported modules and creates a dictionary definition for them
# Dictionary contains the following fields: file_name, test_id, params, capabilities
def create_definitions():
    script_id = 0
    for module in modules:
        definitions.append(dict(
            file_name=module.__name__.removeprefix('a2u_appiumrun.tests.'),
            script_id=script_id,
            definition=getattr(module, 'definition', None),
            capabilities=getattr(module, 'capabilities', None),
        ))
        script_id += 1


# Gets the definition of a test module at the specified index
def get_definition(test_id):
    if test_id < len(definitions):
        return definitions[test_id]
    else:
        return None


#  Runs the test at the index with test_id
def run_test(request_body):
    test_id = request_body['test_id']

    if test_id > len(definitions):
        raise IndexError(f'Provided test_id ({test_id}) is out of range.')

    # explicitly declares inputData declaration as global
    user_input = request_body['params']
    definition = getattr(modules[test_id], 'definition', None)
    try:
        if isinstance(user_input, dict) and definition is not None:
            definition['parameters'] = user_input
    except KeyError:
        print('Attempt to access script parameters failed. Parameters were missing.')
        print('   Provided input: ' + str(user_input))
        print('   Script definition: ' + str(definition))

    main_func = getattr(modules[test_id], 'main', None)
    if callable(main_func):
        return main_func()


'''
# Given a module and a function name as a String, runs a function and returns its value
def call_function_from_module(module, function_name):
    func = getattr(module, function_name, None)
    if callable(func):
        return func()
'''
