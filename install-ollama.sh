#!/bin/bash

# Update Homebrew and install Ollama
echo "Updating Homebrew and installing Ollama..."
curl -fsSL https://ollama.com/install.sh | sh

# Check if Ollama was installed successfully
if ! command -v ollama &> /dev/null
then
    echo "Ollama installation failed. Please check your Homebrew setup."
    exit 1
fi

# Download the Llama3 model using Ollama
echo "Downloading the Llama3 model..."
ollama pull llama3

# Check if the Llama3 model was downloaded successfully
if ollama list | grep -q "llama3"; then
    echo "Llama3 model downloaded successfully."
else
    echo "Failed to download the Llama3 model."
    exit 1
fi

# Start Ollama server
echo "Starting Ollama server..."
ollama serve &

# Confirm the server is running
if pgrep -f "ollama serve" > /dev/null; then
    echo "Ollama server is running."
else
    echo "Failed to start Ollama server."
    exit 1
fi

echo "Ollama installation and setup complete."
