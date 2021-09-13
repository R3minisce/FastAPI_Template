FROM python:3.9
COPY . .
RUN pip3 install -r /requirements.txt
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--ssl-keyfile", "/config/key.pem", "--ssl-certfile", "/config/cert.pem", "--reload"]