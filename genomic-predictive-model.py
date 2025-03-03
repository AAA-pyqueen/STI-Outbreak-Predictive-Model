import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import requests

# Update Function for NCBI Open API 3/3/25!!
def fetch_ncbi_data():
    base_url = "https://api.ncbi.nlm.nih.gov/datasets/v1/genome/accession/"
    pathogens = ["Syphilis", "HPV", "HSV", "HIV"]
    
    genomic_data = []
    metadata = []
    
    for pathogen in pathogens:
        response = requests.get(f"{base_url}{pathogen}")
        if response.status_code == 200:
            data = response.json()
            for genome in data.get("genomes", []):
                genomic_data.append(genome.get("sequence"))
                metadata.append({
                    "pathogen": pathogen,
                    "host": genome.get("host"),
                    "collection_date": genome.get("collection_date"),
                    "location": genome.get("location")
                })
    
    genomic_df = pd.DataFrame(genomic_data, columns=["genomic_sequence"])
    metadata_df = pd.DataFrame(metadata)
    return genomic_df, metadata_df

# Load genomic and metadata
def load_data():
    genomic_df, metadata_df = fetch_ncbi_data()
    data = pd.concat([genomic_df, metadata_df], axis=1)
    return data

# Preprocessing function
def preprocess_data(data):
    # Encode categorical variables
    data = pd.get_dummies(data, drop_first=True)
    
    # Split features and target variable
    X = data.drop(columns=['outbreak_label'])  # Adjust based on actual column names
    y = data['outbreak_label']
    
    # Normalize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Define TensorFlow model
def build_model(input_shape):
    model = keras.Sequential([
        keras.layers.Dense(128, activation='relu', input_shape=(input_shape,)),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(1, activation='sigmoid')
    ])
    
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Train and evaluate model
def train_and_evaluate():
    data = load_data()
    X_train, X_test, y_train, y_test = preprocess_data(data)
    
    model = build_model(X_train.shape[1])
    
    # Set default parameters for training
    epochs = 50
    batch_size = 32
    
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test, y_test))
    
    # Predictions
    y_pred = (model.predict(X_test) > 0.5).astype(int)
    
    # Performance Metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print(f'Accuracy: {accuracy:.4f}, Precision: {precision:.4f}, Recall: {recall:.4f}, F1-score: {f1:.4f}')
    
    # Save model
    model.save('infectious_disease_model.h5')
    
    # Plot Training History
    plt.plot(model.history.history['accuracy'], label='accuracy')
    plt.plot(model.history.history['val_accuracy'], label='val_accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    train_and_evaluate()

