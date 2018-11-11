FROM python:3.6

LABEL name="Victoria"
LABEL email="me@vika.space"

COPY ./emonalerts/src/ /app
COPY ./emonalerts/req.txt /app
WORKDIR /app

RUN pip install -r req.txt && chmod +x runner.py && chmod +x runner.py

ENTRYPOINT [ "./runner.py", "default.toml", "credentials.json", "-a", "-v"]