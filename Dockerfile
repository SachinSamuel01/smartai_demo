# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Install curl and any other dependencies you need
RUN apt-get update && apt-get install -y curl

# Install ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . /app

# Install application dependencies
RUN pip install -r requirements.txt

RUN nohup ollama serve & sleep 20

# Pull the Mistral model
RUN ollama pull mistral

# Expose the port that your application runs on
EXPOSE 3001

# Run the application
CMD ["python", "main.py"]
