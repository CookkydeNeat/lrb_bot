# Use an official Python runtime as the base image
FROM python:3.8
    
COPY . /app

WORKDIR /app

RUN pip install install requests discord asyncio nest_asyncio python-dotenv instaloader

# Add labels for better maintainability
LABEL maintainer="Cookky <cookky.neat@gmail.com>"
LABEL version="1.0"
LABEL description="Dockerfile for running a Discord.js bot"
