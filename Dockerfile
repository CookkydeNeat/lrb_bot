# Use an official Python runtime as the base image
FROM node:latest
    
COPY . /app

WORKDIR /app

RUN npm install --production  
    
# Add labels for better maintainability
LABEL maintainer="Cookky <cookky.neat@gmail.com>"
LABEL version="1.0"
LABEL description="Dockerfile for running a Discord.js bot"