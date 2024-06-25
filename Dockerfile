# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Install curl and any other dependencies you need
RUN apt-get update && apt-get install -y curl

# Install ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Start the ollama service in the background
RUN nohup ollama serve & sleep 5

# Pull the Mistral model
RUN ollama pull mistral

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . /app

# Install application dependencies
RUN pip install -r requirements.txt

# Expose the port that your application runs on
EXPOSE 3001

# Run the application
CMD ["python", "main.py"]
