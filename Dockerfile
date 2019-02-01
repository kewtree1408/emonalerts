FROM python:3.7.2-alpine3.8

LABEL name="Victoria"
LABEL email="me@vika.space"

COPY ./src/ /app
WORKDIR /app
RUN pip install -r req.txt && chmod +x runner.py
ARG TOML
ARG EMAIL

RUN echo ${TOML}
RUN echo ${EMAIL}

ENTRYPOINT ["./runner.py", ${TOML}, ${EMAIL}, "-a", "-v"]
