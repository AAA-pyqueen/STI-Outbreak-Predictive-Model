import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Function to generate a heatmap of correlation between features
def plot_correlation_heatmap(data):
    plt.figure(figsize=(10, 6))
    heatmap = sns.heatmap(data.corr(), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Feature Correlation Heatmap")
    st.pyplot(plt)

# Function to create an interactive histogram of outbreak predictions
def plot_prediction_distribution(predictions):
    fig = px.histogram(predictions, x="Predicted", title="Outbreak Prediction Distribution", color="Predicted")
    st.plotly_chart(fig)

# Function to create a scatter plot of outbreaks by location
def plot_outbreak_locations(data):
    if "latitude" in data.columns and "longitude" in data.columns:
        fig = px.scatter_geo(
            data, lat="latitude", lon="longitude", color="pathogen",
            title="Geographic Distribution of STI Outbreaks",
            hover_name="location"
        )
        st.plotly_chart(fig)
    else:
        st.warning("Latitude and Longitude data is missing.")

# Function to display model performance metrics
def plot_model_performance(history):
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    # Accuracy plot
    ax[0].plot(history.history["accuracy"], label="Train Accuracy")
    ax[0].plot(history.history["val_accuracy"], label="Validation Accuracy")
    ax[0].set_title("Model Accuracy Over Epochs")
    ax[0].set_xlabel("Epochs")
    ax[0].set_ylabel("Accuracy")
    ax[0].legend()

    # Loss plot
    ax[1].plot(history.history["loss"], label="Train Loss")
    ax[1].plot(history.history["val_loss"], label="Validation Loss")
    ax[1].set_title("Model Loss Over Epochs")
    ax[1].set_xlabel("Epochs")
    ax[1].set_ylabel("Loss")
    ax[1].legend()

    st.pyplot(fig)
