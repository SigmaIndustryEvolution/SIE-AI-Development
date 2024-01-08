from flask import Flask, request
from flask_cors import CORS
from multi_view_prediction import predictDoorFormData
import time
import cv2
import numpy

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/images', methods=['POST'])
def predictMultiView():
    view1_Image = cv2.cvtColor(cv2.imdecode(numpy.frombuffer(request.files.get('view1').read(), numpy.uint8), cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
    predictionDictionary = predictDoorFormData(view1_Image)
    return predictionDictionary


"""
For multi-input prediction

def predictMultiView():
    view1_Image = cv2.cvtColor(cv2.imdecode(numpy.frombuffer(request.files.get('view1').read(), numpy.uint8), cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
    view2_Image = cv2.cvtColor(cv2.imdecode(numpy.frombuffer(request.files.get('view2').read(), numpy.uint8), cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
    view3_Image = cv2.cvtColor(cv2.imdecode(numpy.frombuffer(request.files.get('view3').read(), numpy.uint8), cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
    predictionDictionary = predictDoorFormData(view1_Image, view2_Image, view3_Image)
    return predictionDictionary

"""




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)