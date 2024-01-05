import os
import pandas as pd
import re

def findFiles(root_dir, files):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for file in filenames:
            files.append(file)
        # Print the current directory

def writeToCsv(data, filename, part):
    # Define the filename of the existing Excel file
    categories = ["filename", "class"]
    df = pd.DataFrame(data, columns = categories)

    xlsxPath = os.path.join("excel", "single-view", "train-test", part, "xlsx")
    csvPath = os.path.join("excel", "single-view", "train-test", part, "csv")

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

def SetClassesAndParts(root):
    classes = os.listdir(root) # gets a list of all classes from data
    pathToParts = os.path.join(root, classes[0])
    parts = os.listdir(pathToParts) # gets a list of all parts from data
    return classes, parts

if __name__ == "__main__":
    # To get all classes into a fileslist
    root = 'data'
    classes, parts = SetClassesAndParts(root)
    source_dir = r'data-train-test'

    for set in ["train", "test"]:
        for part in parts:
            root_directory = os.path.join(source_dir, set, part) # Replace with your root directory path
            filename = "single-view-" + part + "-" + set + ".xlsx" # filename for the .xlsx and .csv
            files = []
            findFiles(root_directory, files)
            data = []
            for i in files:
                temp = [i, returnClassName(i, classes)]
                data.append(temp)
            writeToCsv(data, filename, part)
            