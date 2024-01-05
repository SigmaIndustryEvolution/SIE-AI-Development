import splitfolders
import os
import shutil

def SetClassesAndParts(root):
    classes = os.listdir(root) # gets a list of all classes from data
    pathToParts = os.path.join(root, classes[0])
    parts = os.listdir(pathToParts) # gets a list of all parts from data
    return classes, parts


def SplitIntoTrainValTest(source, destination, classes, parts):

    # Path(__file__).parents[3] 

    random_int = 403
    for part in parts:
        fullPathToSource = os.path.join("data-parts-classes", part) 
        fullPathToDestination = os.path.join( "data-train-val-test-one-folder")
        splitfolders.ratio(
                        fullPathToSource, # The location of dataset
                        output=fullPathToDestination, # The output location
                        seed=random_int, # The number of seed
                        ratio=(.7, .2, .1), # The ratio of splited dataset
                        group_prefix=None, # If your dataset contains more than one file like ".jpg", ".pdf", etc
                        move=False # If you choose to move, turn this into True
        )

    
    train_path = os.path.join(destination, "train")
    val_path = os.path.join(destination, "val") # the name is just "val" since split-folders doesn't have an option to name it "test"
    test_path = os.path.join(destination, "test")
    paths = [train_path, val_path, test_path]


    # puts all files into only three folders
    for path in paths:
        for root, directories, files in os.walk(path):
            for file in files:
                source_path = os.path.join(root, file)
                destination_path = os.path.join(path, file)
                shutil.move(source_path, destination_path) # use .move or .copy
        for classname in classes:
            os.rmdir(os.path.join(path, classname))


if __name__ == '__main__':
    root = r'data'
    rootPartsClasses = r'data-parts-classes'
    newDirectoryName = r'data-train-val-test-one-folder'
    if not os.path.exists(newDirectoryName):
        os.mkdir(newDirectoryName)
    classes, parts = SetClassesAndParts(root)
    SplitIntoTrainValTest(rootPartsClasses, newDirectoryName, classes, parts)
    