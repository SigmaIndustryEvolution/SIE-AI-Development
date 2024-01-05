import os
import shutil

if __name__ == '__main__':
    inputDirectory = r'data-train-val-test-one-folder'
    outputDirectory = r'data-train-test-one-folder'
    if not os.path.exists(outputDirectory):
        os.mkdir(outputDirectory)
        os.mkdir(os.path.join(outputDirectory, "train"))
        os.mkdir(os.path.join(outputDirectory, "test"))

    pathTrainInput = os.path.join(inputDirectory, "train")
    pathTrainOutput = os.path.join(outputDirectory, "train")

    pathValInput = os.path.join(inputDirectory, "val")

    pathTestInput = os.path.join(inputDirectory, "test")
    pathTestOutput = os.path.join(outputDirectory, "test")

    filesList = os.listdir(pathTrainInput)
    for file_name in filesList:
        full_file_name = os.path.join(pathTrainInput, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, pathTrainOutput)

    filesList = os.listdir(pathValInput)     
    for file_name in filesList:
        full_file_name = os.path.join(pathValInput, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, pathTrainOutput)

    filesList = os.listdir(pathTestInput)
    for file_name in filesList:
        full_file_name = os.path.join(pathTestInput, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, pathTestOutput)

        