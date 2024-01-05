import os
import re
import shutil

def SetClassesAndParts(root):
    classes = os.listdir(root) # gets a list of all classes from data
    pathToParts = os.path.join(root, classes[0])
    parts = os.listdir(pathToParts) # gets a list of all parts from data
    return classes, parts

def CopyFilesToNewFolders(source, destination, classes, parts):
    for dirpath, directories, files in os.walk(source):
        for file in files:
            for partName in parts:
                for className in classes:
                    combinationString = f"{className}_{partName}"
                    match = re.search(combinationString, file) # finds what type of part it is
                    if match:
                        source_path = os.path.join(dirpath, file)
                        destination_path = os.path.join(destination, partName, className, file)
                        shutil.copy(source_path, destination_path) # use .move or .copy

def CreateEmptyDirectoriesPartsClasses(newDirectoryName, classes, parts):
    
    for partName in parts:

        pathToPart = os.path.join(newDirectoryName, partName)
        
        # Check if the directory already exists, and create one if it doesn't
        if not os.path.exists(pathToPart):
            os.makedirs(pathToPart)

        for className in classes:
            pathToPartAndClass = os.path.join(newDirectoryName, partName, className)
        
            # Check if the directory already exists, and create one if it doesn't
            if not os.path.exists(pathToPartAndClass):
                os.makedirs(pathToPartAndClass)
            
            
if __name__ == '__main__':
	# Calling main() function
    root = r'data'
    newDirectoryName = r'data-parts-classes'
    classes, parts = SetClassesAndParts(root)
    CreateEmptyDirectoriesPartsClasses(newDirectoryName, classes, parts)
    CopyFilesToNewFolders(root, newDirectoryName, classes, parts)
 