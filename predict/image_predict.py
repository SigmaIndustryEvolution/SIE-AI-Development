from keras.models import load_model
import cv2
import numpy as np
from prediction_tools import *
import sys

model = load_model("model/model_back-panels.h5")

def predictDoorFormData(front, back, side):
    classList = getFixedClassList()
    image_set = prepareImage(np.asarray(front))
    predictions = model.predict(image_set, verbose = 0)
    return dict(map(lambda i,j : (i,j) , classList, predictions[0].tolist()))

