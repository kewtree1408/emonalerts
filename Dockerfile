FROM python:3.6

LABEL name="Victoria"
LABEL email="me@vika.space"

COPY ./src/ /app
WORKDIR /app
RUN pip install -r req.txt && chmod +x runner.py

ENTRYPOINT [ "./runner.py", "success.toml", "credentials.json", "-a", "-v"]