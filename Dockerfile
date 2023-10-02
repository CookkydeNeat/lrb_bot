# Use an official Python runtime as the base image
FROM python:latest
    
COPY . /app

WORKDIR /app

RUN pip install requests, time, discord, sys, asyncio, threading, nest_asyncio, math, os, dotenv, pyppeteer
RUN apt-get install -y wget
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

# Add labels for better maintainability
LABEL maintainer="Cookky <cookky.neat@gmail.com>"
LABEL version="1.0"
LABEL description="Dockerfile for running a Discord.js bot"