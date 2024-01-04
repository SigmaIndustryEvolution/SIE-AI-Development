FROM jjanzic/docker-python3-opencv 

ADD *.py /opt/predict/
COPY model/ /opt/predict/model/

EXPOSE 8000

RUN pip3 install flash flask_cors keras grpcio==1.57.0 tensorflow

WORKDIR /opt/predict
CMD [ "python3", "/opt/predict/rest_server.py" ]
