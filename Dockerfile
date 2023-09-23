# Use an official Python runtime as the base image
FROM python:latest
    
COPY . /app

WORKDIR /app

  
<<<<<<< HEAD
<<<<<<< HEAD
RUN pip install requests, json, time, discord, sys, asyncio, threading, nest_asyncio, math, os, dotenv, selenium

=======
RUN pip install requests discord asyncio nest_asyncio  pyppeteer python-dotenv
>>>>>>> 5fe87268faa8e50f64e6c82e2a704c0309993219
=======
RUN pip install requests discord asyncio nest_asyncio  pyppeteer python-dotenv
>>>>>>> 5fe87268faa8e50f64e6c82e2a704c0309993219

# Add labels for better maintainability
LABEL maintainer="Cookky <cookky.neat@gmail.com>"
LABEL version="1.0"
LABEL description="Dockerfile for running a Discord.js bot"