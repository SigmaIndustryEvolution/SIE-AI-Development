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
    frontImage = cv2.cvtColor(cv2.imdecode(numpy.frombuffer(request.files.get('front').read(), numpy.uint8), cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
    backImage = cv2.cvtColor(cv2.imdecode(numpy.frombuffer(request.files.get('back').read(), numpy.uint8), cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
    sideImage = cv2.cvtColor(cv2.imdecode(numpy.frombuffer(request.files.get('side').read(), numpy.uint8), cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
    predictionDictionary = predictDoorFormData(frontImage, backImage, sideImage)
    return predictionDictionary

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)