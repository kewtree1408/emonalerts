FROM python:3.7.2-alpine3.8

LABEL name="Victoria"
LABEL email="me@vika.space"

COPY ./src/ /app
RUN pip install -r /app/req.txt && chmod +x /app/runner.py
