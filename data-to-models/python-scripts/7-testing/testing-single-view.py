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


def RescaleAndNormalizeImage(img):
    img = rescale2Minus1And1(img)
    return np.array([cv2.resize(img, (256, 256), cv2.INTER_LANCZOS4)])


if __name__ == '__main__':
    
    classes, parts = SetClassesAndParts()

    models = []
    for part in parts: 
        models.append(load_model(os.path.join("models/single-view", part, f"model_{part}.h5")))
    classDict = {key: 0 for key in classes}

    inputDir = r'test-data-views' # path to where directory is

    i = 0
    for part in parts:
        currentModel = models[i]
        total = 0
        right_answers = 0
        for dirpath, dirnames, files in os.walk(os.path.join(inputDir, part)):
            print(len(files))
            for file in files:
                file_path = os.path.join(dirpath, file)
                img = cv2.imread(file_path,cv2.IMREAD_COLOR)
                img = RescaleAndNormalizeImage(img)
                predictions = currentModel.predict(img, verbose = 0)
                index = int(predictions[0].argmax())

                for className in classes:
                    match = re.search(className, file) # finds what type of part it is
                    if match:
                        if className == classes[index]:
                            classDict[className] += 1
                            right_answers += 1
                            break
                        else:
                            break
                print(LINE_UP, end = LINE_CLEAR)
                total += 1
                print(f"Current accuracy: {round(100*right_answers/total, 2)}%")
                
        print(f"The {part}-model has an accuracy of : {round(100*right_answers/total, 2)}% for this set of images. Number of images in the testset was {total}.")
        for key, value in classDict.items():
            print(f"Accuracy for {key}: { round(100*value / (len(files)/len(classes)), 2) }%")
            classDict[key] = 0
        i += 1 