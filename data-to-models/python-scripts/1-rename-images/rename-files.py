import os
# Script for renaming multiple files
# Goes through each file in map called data and renames it to "className_partName_n.jpg", where n is an integer
def main():
	# change here if needed, directory structure must be ordered in parts and then class names
	LINE_CLEAR = '\x1b[2K'
	LINE_UP = '\033[1A'
	root = r'data' 
	for dirpath, dirnames, files in os.walk(root):
		for i, file in enumerate(files, start=1):
			partName = os.path.basename(dirpath) # Extracting partname from directory name
			className = os.path.basename(os.path.dirname(dirpath)) # Extracting classname from directory name
			newFileName = f'{className}_{partName}_{i}.jpg' 
			pathToDirectoryOfFile = os.path.join(root, className, partName)
			currentFilePath = os.path.join(pathToDirectoryOfFile, file)
			newFilePath = os.path.join(pathToDirectoryOfFile, newFileName)
			
			try:
				print(LINE_UP, end = LINE_CLEAR)
				print("Renaming...")
				os.rename(currentFilePath, newFilePath)
			except:
				print(LINE_UP, end = LINE_CLEAR)
				print("File with that name already exists")
		
if __name__ == '__main__':
	# Calling main() function
	main()