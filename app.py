import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
import plotly.express as px
import folium
from streamlit_folium import folium_static
from api_fetcher import fetch_ncbi_data
from data_processing import preprocess_data
from tensorflow.keras.models import load_model

# Load trained model
MODEL_PATH = "saved_model/infectious_disease_model.h5"
model = load_model(MODEL_PATH)

# Title
st.title("🔬 STI Outbreak Prediction Dashboard")

# Sidebar Navigation
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Choose Mode:", ["📂 Upload Data", "🌍 Fetch Genomic Data", "📊 Predictions", "🗺 Interactive Map", "📝 User Feedback"])

# File Upload Section
if app_mode == "📂 Upload Data":
    st.subheader("Upload Your Dataset for Prediction")
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        user_data = pd.read_csv(uploaded_file)
        st.write("📄 **Uploaded Data Preview:**")
        st.write(user_data.head())

        # Preprocess and predict
        try:
            X_train, X_test, y_train, y_test = preprocess_data(user_data)
            predictions = (model.predict(X_test) > 0.5).astype(int)
            
            # Display Predictions
            results_df = pd.DataFrame({"Actual": y_test, "Predicted": predictions.flatten()})
            st.subheader("📊 Prediction Results")
            st.write(results_df.head())

            # Plot Predictions
            fig = px.histogram(results_df, x="Predicted", title="Outbreak Prediction Distribution")
            st.plotly_chart(fig)

        except Exception as e:
            st.error(f"⚠ Error in processing: {e}")

# Fetch NCBI Data Section
elif app_mode == "🌍 Fetch Genomic Data":
    st.subheader("Fetch Real-Time Genomic Data from NCBI")
    if st.button("Fetch Data"):
        genomic_data = fetch_ncbi_data()
        st.write("🧬 **Fetched Genomic Data Preview:**")
        st.write(genomic_data.head())

# Prediction Dashboard Section
elif app_mode == "📊 Predictions":
    st.subheader("Run Outbreak Predictions")

    if st.button("Predict on Sample Data"):
        sample_data = pd.DataFrame({
            "pathogen": ["Syphilis", "HPV", "HSV", "HIV"],
            "location": ["USA", "Canada", "Mexico", "UK"],
            "latitude": [37.7749, 45.4215, 19.4326, 51.5074],
            "longitude": [-122.4194, -75.6972, -99.1332, -0.1278],
            "outbreak_label": [1, 0, 1, 0]
        })

        X_train, X_test, y_train, y_test = preprocess_data(sample_data)
        predictions = (model.predict(X_test) > 0.5).astype(int)

        results_df = sample_data.copy()
        results_df["Predicted"] = predictions.flatten()

        st.write(results_df[["pathogen", "location", "Predicted"]])

        # Map Predictions
        fig = px.scatter_geo(results_df, lat="latitude", lon="longitude", 
                             color="Predicted", title="Outbreak Prediction Map",
                             hover_name="location", size_max=10)
        st.plotly_chart(fig)

# Interactive Map Section
elif app_mode == "🗺 Interactive Map":
    st.subheader("🗺 STI Outbreak Heatmap")

    sample_data = pd.DataFrame({
        "pathogen": ["Syphilis", "HPV", "HSV", "HIV"],
        "location": ["USA", "Canada", "Mexico", "UK"],
        "latitude": [37.7749, 45.4215, 19.4326, 51.5074],
        "longitude": [-122.4194, -75.6972, -99.1332, -0.1278],
        "outbreak_label": [1, 0, 1, 0]
    })

    map_data = sample_data[sample_data["outbreak_label"] == 1]  # Filter only outbreaks
    outbreak_map = folium.Map(location=[39.8283, -98.5795], zoom_start=3)

    for _, row in map_data.iterrows():
        folium.Marker([row["latitude"], row["longitude"]],
                      popup=f"{row['pathogen']} Outbreak in {row['location']}",
                      icon=folium.Icon(color="red")).add_to(outbreak_map)

    folium_static(outbreak_map)

# User Feedback Section
elif app_mode == "📝 User Feedback":
    st.subheader("📝 Provide Feedback on Predictions")

    feedback_name = st.text_input("Your Name (Optional)")
    feedback_comment = st.text_area("What issue did you notice?")
    feedback_correct_label = st.radio("Was the prediction correct?", ["Yes", "No", "Not Sure"])

    if st.button("Submit Feedback"):
        with open("feedback_log.txt", "a") as f:
            f.write(f"Name: {feedback_name}\n")
            f.write(f"Feedback: {feedback_comment}\n")
            f.write(f"Correct Prediction: {feedback_correct_label}\n")
            f.write("="*50 + "\n")

        st.success("✅ Thank you for your feedback!")

# Footer
st.markdown("---")
st.caption("Developed by Aquesha Addison | Powered by TensorFlow & Streamlit")