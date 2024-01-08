from keras.models import load_model
import cv2
from PIL import Image
import os
import numpy as np
import re
from ..tools import SetClassesAndParts

LINE_CLEAR = '\x1b[2K'
LINE_UP = '\033[1A'

def rescale2Minus1And1(img):
    img = img.astype(np.float32) / 255.0
    img = (img - 0.5) * 2
    return img 

def RescaleAndNormalizeImage(filePath):
    img = cv2.imread(filePath, cv2.IMREAD_COLOR)
    img = rescale2Minus1And1(img)
    return np.array([cv2.resize(img, (256, 256), cv2.INTER_LANCZOS4)])
  
if __name__ == '__main__':
    
    # load model
    multi_view = load_model(r'models/multi-view/multi-view.h5')

    root = r'data'
    inputDir = r'test-data-views'
    classes, parts = SetClassesAndParts()

    classDict = {key: 0 for key in classes}

    pathsToImages = []
    i = 0
    
    pathToImages = []
    for part in parts:
        images = []
        currentPath = os.path.join(inputDir, part)
        for filename in os.listdir(currentPath):
            filepath = os.path.join(currentPath, filename)
            if os.path.isfile(filepath):
                images.append(filepath)
        pathsToImages.append(images)

    right_answer = 0
    total = 0
    
    # assumes that the number of images in each folder is the same
    numberOfImages = len(pathsToImages[0])
    numberOfImagesPerClass = numberOfImages//len(classes)
    count = 1
    
    for i in range(numberOfImages):
        testSetOfImages = []
        for j in range(len(pathsToImages)):
            testSetOfImages.append(RescaleAndNormalizeImage(pathsToImages[j][i]))
        
        predictions = multi_view.predict(testSetOfImages, verbose = 0)
        index = int(predictions[0].argmax())

        for class_name in classes:
            match = re.search(class_name, pathsToImages[j][i]) # finds what type of part it is
            if match:
                if class_name == classes[index]:
                    classDict[class_name] += 1
                    right_answer += 1
                    total += 1
                    break
                else:
                    total += 1
                    break
        print(LINE_UP, end = LINE_CLEAR)
        print(f"Testing: {i + 1} out of {numberOfImages}, Total number of right answers: {right_answer} Current accuracy: {round(100*right_answer/total, 2)}%")
        count += 1
        
                

    print(f"The multi-view-model has an accuracy of: {round(100*right_answer/total, 2)}% for this set of images. Number of images in the testset was {count - 1}.")
    for key, value in classDict.items():
        print(f"Accuracy for {key}: {round(100*value / numberOfImagesPerClass, 2)}%")