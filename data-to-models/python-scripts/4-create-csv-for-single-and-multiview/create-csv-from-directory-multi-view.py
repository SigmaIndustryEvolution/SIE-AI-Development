import os
import pandas as pd
import re
import random

def findFiles(root_dir, partsAndFilesDictionary, parts):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for file in filenames:
            part_name = returnPartName(file, parts)
            partsAndFilesDictionary[part_name].append(file)
    

def writeToCsv(data, filename, classes):
    # Define the filename of the existing Excel file
    categories = classes + ["class"]
    df = pd.DataFrame(data, columns = categories)
    xlsxPath = os.path.join("excel", "multi-view", "xlsx")
    csvPath = os.path.join("excel", "multi-view", "csv")

    if not os.path.exists(xlsxPath):
        os.makedirs(xlsxPath)
    if not os.path.exists(csvPath):
        os.makedirs(csvPath)
    
    path_to_excel_files_xlsx = xlsxPath
    path_to_excel_files_csv = csvPath
    full_path = os.path.join(path_to_excel_files_xlsx, filename)
    writer = pd.ExcelWriter(full_path, engine='xlsxwriter')

    df.to_excel(writer, sheet_name="listOfCombinations")

    writer.close()
    # Save as CSV (.csv)
    csv_filename = os.path.splitext(filename)[0] + ".csv"
    csv_full_path = os.path.join(path_to_excel_files_csv, csv_filename)
    df.to_csv(csv_full_path, index=False)

def returnClassName(filename, classes):
    # empty dictionary to add a combination. This dict is then used to match against new_combinations
        for className in classes:
            match = re.search(className, filename) # finds what type of door it is
            if match:
                return className
        return "no class"

def returnPartName(filename, parts):
    # empty dictionary to add a combination. This dict is then used to match against new_combinations
        for part in parts:
            match = re.search(part, filename) # finds what type of door it is
            if match:
                return part
        return "no part"

def shuffleList(categories):
    # empty dictionary to add a combination. This dict is then used to match against new_combinations
        for part in categories:
            random.Random(3).shuffle(parts[part]) # using random.Random to replicate result for all lists 

def SetClassesAndParts(root):
    classes = os.listdir(root) # gets a list of all classes from data
    pathToParts = os.path.join(root, classes[0])
    parts = os.listdir(pathToParts) # gets a list of all parts from data
    return classes, parts

if __name__ == "__main__":
    root = 'data'
    classes, parts = SetClassesAndParts(root)
    root_directory = r'data-train-val-test-one-folder'
    for set in ["train", "val", "test"]:
        data = []
        currentDirectory = os.path.join(root_directory, set)
        fileName = f"multi-view-{set}.xlsx"
        partsAndFilesDictionary  = {key: [] for key in parts}
        findFiles(currentDirectory, partsAndFilesDictionary, parts)
        for i in range(len(partsAndFilesDictionary[parts[0]])):
            temp = []
            for part in parts:
                temp.append(partsAndFilesDictionary[part][i])
            temp.append(returnClassName(temp[0], classes))
            data.append(temp)
        writeToCsv(data, fileName, parts)

    
    