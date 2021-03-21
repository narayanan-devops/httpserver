FROM python:3.8-slim-buster
RUN apt update && apt -y install libcairo2-dev
RUN apt-get update && apt-get install build-essential -y
RUN mkdir /app 
ADD httpserver.py /app
ADD requirements.txt /app
RUN pip3 install -r /app/requirements.txt 
EXPOSE 5000
ENTRYPOINT [ "python" ] 
CMD [ "/app/httpserver.py" ] 
