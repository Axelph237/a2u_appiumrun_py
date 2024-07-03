import os
import importlib


def beautify_filename(name):
    return name.removesuffix('.py').replace('_', ' ').title()


def import_modules_from_directory(directory):
    modules = []

    for filename in os.listdir(directory):
        if filename.endswith('.py') and filename != '__init__.py':
            # Remove suffix and create path
            module_name = filename[:-3]
            module_path = f'tests.{module_name}'
            # Import script as a module
            module = importlib.import_module(module_path)
            modules.append(module)
    return modules


def call_function_from_module(module, function_name):
    func = getattr(module, function_name, None)
    if callable(func):
        func()


def get_parameters_from_module(module):
    return getattr(module, 'input_parameters', None)


def main():
    tests = []

    tests_directory = os.path.join(os.getcwd(), 'tests')
    modules = import_modules_from_directory(tests_directory)
    test_id = 0
    for module in modules:
        tests.append(dict(
            test=module.__name__.removeprefix('tests.'),
            id=test_id,
            params=get_parameters_from_module(module),
        ))
        test_id += 1

    print(tests)


if __name__ == '__main__':
    main()
