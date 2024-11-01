# Use a lightweight Python image
FROM python:3.10-slim

# Install system dependencies, Chrome, and Chromedriver
RUN apt-get update && apt-get install -y curl gnupg && \
    curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable unzip && \
    curl -sS -o /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin && \
    rm /tmp/chromedriver.zip

# Set environment variables
ENV DRIVER_PATH="/usr/local/bin/chromedriver"

# Set up working directory
WORKDIR /app

# Copy project files
COPY src /app/src
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the command to run the scraper
CMD ["python", "/app/src/linkedin_scraper.py"]
