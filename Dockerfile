# Use an official Python runtime as the base image
FROM python:latest
    
# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt
    
# Add labels for better maintainability
LABEL maintainer="Cookky <cookky.neat@gmail.com>"
LABEL version="1.0"
LABEL description="Dockerfile for running a Discord.py bot"