#!/bin/bash

echo "🚀 Setting up the STI Outbreak Predictive Model Web App..."

# Set up environment
echo "🔹 Creating virtual environment..."
python -m venv venv
source venv/bin/activate  # For macOS/Linux
# source venv/Scripts/activate  # For Windows (uncomment if running on Windows)

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Generate secret key 
if [ ! -f "secret.key" ]; then
    echo "🔑 Generating encryption key..."
    python -c "from cryptography.fernet import Fernet; key = Fernet.generate_key(); open('secret.key', 'wb').write(key)"
    echo "✅ Secret key generated!"
fi

# Encrypt API key
if [ ! -f "encrypted_api.key" ]; then
    echo "🔒 Encrypting API key..."
    read -s -p "Enter your NCBI API Key: " API_KEY
    python -c "
from cryptography.fernet import Fernet;
with open('secret.key', 'rb') as key_file: secret_key = key_file.read();
cipher = Fernet(secret_key);
encrypted_api_key = cipher.encrypt(b'$API_KEY');
with open('encrypted_api.key', 'wb') as encrypted_file: encrypted_file.write(encrypted_api_key);
"
    echo "✅ API Key encrypted and saved!"
fi

# Run the App
echo "🚀 Starting the web app..."
python app.py
