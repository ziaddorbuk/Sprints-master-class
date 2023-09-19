# Use the official Python image as the base image
FROM python:3.8-slim

ENV POSTGRES_DB bookstore
ENV POSTGRES_USER username
ENV POSTGRES_PASSWORD password
ENV POSTGRES_HOST postgres

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
