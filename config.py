import os
from cryptography.fernet import Fernet

# Load secret key
with open("secret.key", "rb") as key_file:
    secret_key = key_file.read()

cipher = Fernet(secret_key)

# Load and decrypt the API key
with open("encrypted_api.key", "rb") as encrypted_file:
    encrypted_api_key = encrypted_file.read()

NCBI_API_KEY = cipher.decrypt(encrypted_api_key).decode()

# 🌍 Default Map Settings
DEFAULT_LATITUDE = 39.8283
DEFAULT_LONGITUDE = -98.5795
DEFAULT_ZOOM_LEVEL = 4

# 📊 Model Settings
MODEL_PATH = "saved_model/infectious_disease_model.h5"
BATCH_SIZE = 32
EPOCHS = 50
LEARNING_RATE = 0.001

# 📝 File Paths
FEEDBACK_LOG = "feedback_log.txt"

# ⚠️ Debug Mode
DEBUG_MODE = True
