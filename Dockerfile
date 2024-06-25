FROM python:3.8-slim

# Install necessary packages
RUN apt-get update && apt-get install -y curl

# Install ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Pull the Mistral model
RUN ollama pull mistral

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . /app

# Install application dependencies
RUN pip install -r requirements.txt

# Run the application
CMD ["python", "main.py"]
