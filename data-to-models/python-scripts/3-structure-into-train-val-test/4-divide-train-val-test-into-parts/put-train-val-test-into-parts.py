import os
import shutil
import re
# Function to rename multiple files

def SetClassesAndParts(root):
    classes = os.listdir(root) # gets a list of all classes from data
    pathToParts = os.path.join(root, classes[0])
    parts = os.listdir(pathToParts) # gets a list of all parts from data
    return classes, parts


def copy_all_files_to_folders(source_directory, destination_directory, part):
    for dirpath, directories, files in os.walk(source_directory):
        for file in files:
            match = re.search(part, file) # finds what type of part it is
            if match:
                source_path = os.path.join(dirpath, file)
                destination_path = os.path.join(destination_directory, part, file)
                shutil.copy(source_path, destination_path) # use .move or .copy

def main():
    root = 'data'
    source_directory = r'data-train-val-test-one-folder'
    destination_directory = r'data-train-val-test'
    
    classes, parts = SetClassesAndParts(root)
    if not os.path.exists(destination_directory):
        os.mkdir(destination_directory)
    for set in ["train", "val", "test"]:
        if not os.path.exists(os.path.join(destination_directory, set)):
            os.mkdir(os.path.join(destination_directory, set))
        for part in parts:
            if not os.path.exists(os.path.join(destination_directory, set, part)):
                os.mkdir(os.path.join(destination_directory, set, part))
            copy_all_files_to_folders(os.path.join(source_directory, set), os.path.join(destination_directory, set), part)

    # Driver Code
if __name__ == '__main__':
    # Calling main() function
    main()