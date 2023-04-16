# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy the current directory contents into the container at /app
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y ffmpeg
RUN pip install -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV FLASK_APP=app.py

# Run the command to start the server
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app