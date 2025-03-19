# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libasound2-dev \
    portaudio19-dev \
    tk \
    tcl \
    xvfb \
    x11vnc \
    fluxbox \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the VNC port
EXPOSE 5900

# Set the DISPLAY environment variable
ENV DISPLAY=:99

# Run the application with Xvfb and x11vnc
CMD ["/bin/sh", "-c", "Xvfb :99 -screen 0 1024x768x16 & fluxbox & x11vnc -display :99 -forever -nopw -listen 0.0.0.0 -xkb & python baseball_name_game2.py"] 