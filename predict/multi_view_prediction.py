from keras.models import load_model
import cv2
import numpy as np
from prediction_tools import *
import sys

model = load_model("model/multi-view.h5")

# load model
def predictDoorBase64(image_dictionary):

    classList = getFixedClassList()

    sys.stderr.write("CLASSLIST {0}".format(classList))
    decoded_images = [
        cv2.cvtColor(cv2.imdecode(strToImage("front", image_dictionary), cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB),
        cv2.cvtColor(cv2.imdecode(strToImage("back", image_dictionary), cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB),
        cv2.cvtColor(cv2.imdecode(strToImage("side", image_dictionary), cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB),
    ]
    image_set = [prepareImage(i) for i in decoded_images]
    predictions = model.predict(image_set, verbose=0)
    sys.stderr.write("PREDICTIONS {0}".format(predictions))
    index = int(predictions[0].argmax())
    return f"{classList[index].upper()}"

def predictDoorFormData(front, back, side):
    classList = getFixedClassList()
    image_set = [prepareImage(np.asarray(front)), prepareImage(np.asarray(back)), prepareImage(np.asarray(side))]
    predictions = model.predict(image_set, verbose = 0)
    return dict(map(lambda i,j : (i,j) , classList, predictions[0].tolist()))

