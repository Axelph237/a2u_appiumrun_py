import os


# Takes the filename and changes it as the following:
# file_name -> 'File Name'
def beautify_filename(name):
    return name.removesuffix('.py').replace('_', ' ').title()


# Get the directory of the current script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Define a relative path to a file
relative_path = 'tests\\'

# Construct the full path
directory = os.path.join(script_directory, relative_path)

print("File directory:")
print(directory)

print()
print("Scripts:")
# List all files in the directory and subdirectories
scripts = []
for root, dirs, filenames in os.walk(directory):
    for filename in filenames:
        print(beautify_filename(filename))

