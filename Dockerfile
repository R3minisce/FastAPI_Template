FROM python:3.9
COPY . .
RUN pip3 install -r /requirements.txt
CMD [ "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000", "--ssl-keyfile", "/config/key.pem", "--ssl-certfile", "/config/cert.pem", "--reload"]