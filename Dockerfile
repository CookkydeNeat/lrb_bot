# Use an official Python runtime as the base image
FROM python:latest
    
COPY . /app

WORKDIR /app
  
RUN pip install requests discord asyncio threading _asyncio python-dotenv selenium

# Add labels for better maintainability
LABEL maintainer="Cookky <cookky.neat@gmail.com>"
LABEL version="1.0"
LABEL description="Dockerfile for running a Discord.js bot"