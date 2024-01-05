import os
import shutil
import re

def SetClassesAndParts(root):
    classes = os.listdir(root) # gets a list of all classes from data
    parts = os.listdir(os.path.join(root, classes[0])) # gets a list of all parts from data
    return classes, parts

root = r'data'
inputDirectory = r'test-data'
outputDirectory = r'test-data-views'

classes, parts =  SetClassesAndParts(root)

for part in parts:      
    # Check if the directory already exists, and create one if it doesn't
    if not os.path.exists(os.path.join(outputDirectory, part)):
        os.makedirs(os.path.join(outputDirectory, part))


for dirpath, directories, files in os.walk(inputDirectory):
        for file in files:
            for part in parts:
                match = re.search(part, file) # finds what type of part it is
                if match:
                    for class_name in classes:
                        match = re.search(class_name, file) # finds what type of part it is
                        if match:
                            source_path = os.path.join(dirpath, file)
                            destination_path = os.path.join(outputDirectory, part, file)
                            shutil.copy(source_path, destination_path) # use .move or .copy