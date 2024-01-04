from keras.models import load_model
import cv2
import numpy as np
from prediction_tools import *


front = load_model(r'C:\Users\73351374\sigma\kod\models\sigma-demo\front-panels\front-panels_model_2.h5')

# load model
def predict(image_string):

    classDictionary = getClasses()
    # Create an in-memory file-like object
    
    img = cv2.imdecode(strToImage(image_string), cv2.IMREAD_COLOR)
    norm_img = (img / 127.5) - 1.0
    scaled_norm_img = np.array([cv2.resize(norm_img, (256, 256), cv2.INTER_LANCZOS4)])
    predictions = front.predict(scaled_norm_img, verbose = 0)
    index = int(predictions[0].argmax())
    return f"{classDictionary[index].upper()}"
