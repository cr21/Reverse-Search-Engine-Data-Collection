# light setup
FROM python:3.9.15-slim-bullseye

COPY . /searchengine

WORKDIR /searchengine

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8080
RUN ["python","app.py"]