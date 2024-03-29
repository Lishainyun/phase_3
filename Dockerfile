# syntax=docker/dockerfile:1

FROM python:3.10-alpine
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt \
    pip install flask_cors
COPY . .
CMD [ "python3", "app.py"]
