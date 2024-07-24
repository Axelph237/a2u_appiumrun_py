import os
import importlib
import inspect
import unittest

scripts_directory = None
modules = []
definitions = []
initialized = False


# Used to initialize the module's values
# Arguments:
#   directory: the path to import script modules from
def init(directory):
    global scripts_directory, initialized

    try:
        initialized = True
        scripts_directory = directory
        load_scripts()
    except Exception as e:
        initialized = False
        print('Script Handler initialization failed with exception: ' + str(e))


# Loads all script modules found in the tests_directory
def load_scripts():
    global modules, definitions

    if not initialized:
        raise ValueError(f"scripts_directory {scripts_directory} is None. Module may have not been initialized.")

    # Ensuring empty arrays
    definitions.clear()
    modules.clear()

    modules = import_modules(scripts_directory, 'a2u_appiumrun.scripts')
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
# Dictionary contains the following fields: file_name, script_id, definition, capabilities
def create_definitions():
    script_id = 0
    for module in modules:
        definitions.append(dict(
            file_name=inspect.getmodulename(module.__file__),
            script_id=script_id,
            definition=getattr(module, 'definition', None),
            capabilities=getattr(module, 'capabilities', None),
        ))
        script_id += 1


# Gets the definition of a script module at the specified index
def get_definition(script_id):
    if script_id < len(definitions):
        return definitions[script_id]
    else:
        return None


def handle_run_request(request_body):
    script_id = request_body['script_id']

    # Ensure script_id is a valid module
    if script_id > len(definitions):
        raise IndexError(f'Provided script_id ({script_id}) is out of range.')

    process_input(request_body)
    run_test(request_body, script_id)


def process_input(request_body):
    # Get the input parameters from the request, then set them within the script
    # If the script has no definition, or the parameters are empty, raise KeyError
    try:
        request_definition = request_body['definition']
        if request_definition is None:
            raise ValueError()

        definition = getattr(modules[request_body['script_id']], 'definition', None)

        if isinstance(request_definition['parameters'], dict) and definition is not None:
            definition['parameters'] = request_definition['parameters']
    except (KeyError, ValueError):
        # TODO make print statements like these official log statements
        print('[WARN] Attempt to access script parameters failed. Parameters were likely missing.')


#  Runs the script at the index with script_id
def run_test(request_body, script_id):

    # Get all class members of the module
    members = inspect.getmembers(modules[script_id], inspect.isclass)
    # Filter out the classes that are defined in your module, and only accept classes that inherit from TestCase
    classes = [member for name, member in members
               if member.__module__ == modules[script_id].__name__ and issubclass(member, unittest.TestCase)]
    # Only run first TestCase for now
    suite = unittest.TestLoader().loadTestsFromTestCase(classes[0])
    unittest.TextTestRunner(verbosity=2).run(suite)

    # Deprecated main call to script modules
    '''main_func = getattr(modules[script_id], 'main', None)
    if callable(main_func):
        return main_func()'''


'''
# Given a module and a function name as a String, runs a function and returns its value
def call_function_from_module(module, function_name):
    func = getattr(module, function_name, None)
    if callable(func):
        return func()
'''
