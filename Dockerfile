# Use an official Python runtime as the base image
FROM python:latest
    
COPY . /app

WORKDIR /app

RUN pip install requests, time, discord, sys, asyncio, threading, nest_asyncio, math, os, dotenv, selenium

# Add labels for better maintainability
LABEL maintainer="Cookky <cookky.neat@gmail.com>"
LABEL version="1.0"
LABEL description="Dockerfile for running a Discord.js bot"