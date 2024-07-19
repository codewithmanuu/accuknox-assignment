# Use an official Python runtime as the base image
FROM python:3.8-slim

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . /app/
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
