import os

def SetClassesAndParts():
    root = r'data'
    classes = os.listdir(root) # gets a list of all classes from data
    parts = os.listdir(os.path.join(root, classes[0])) # gets a list of all parts from data
    return classes, parts