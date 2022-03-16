# syntax=docker/dockerfile:1
FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN mkdir /newsapp
WORKDIR /newsapp
COPY requirements.txt /newsapp/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /newsapp/