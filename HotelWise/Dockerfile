FROM python:3.9-slim
LABEL maintainer="mdallanegra@icloud.com"

COPY ./requirements.txt /requirements.txt
COPY ./HotelWiseWeb /HotelWiseWeb
WORKDIR /HotelWiseWeb

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt && \
    adduser --disabled-password --no-create-home django-user

ENV PATH="/py/bin:$PATH"

USER django-user