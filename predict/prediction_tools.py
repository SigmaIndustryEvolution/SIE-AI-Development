import base64
import os
import numpy as np
import cv2

# returns a list of the doors based on the directories in the dataset used
def getClasses():
    class_path = r'C:\Users\73351374\sigma\datasets\sigma-demo\images' # path to where directory is
    all_items = os.listdir(class_path)
    print([ item for item in all_items if os.path.isdir(os.path.join(class_path, item))])
    return [ item for item in all_items if os.path.isdir(os.path.join(class_path, item))]

# returns a list with the 5 classes of doors
def getFixedClassList():
    return ['alpha-microrib', 'condoor-st3v', 'crawford-542', 'hormann-spu40', 'novoferm-t45']

# NOT USED
# Input: Part of the door( Front, Back, Side ), Door in base64 format
# Returns: 
def strToImage(partString, image_string):
    png_recovered = base64.b64decode(image_string[partString])
    # Create an in-memory file-like object
    return np.frombuffer(png_recovered, np.uint8)

def prepareImage(imageJPG):
    norm_img = (imageJPG / 127.5) - 1.0
    return np.array([cv2.resize(norm_img, (256, 256), cv2.INTER_LANCZOS4)])