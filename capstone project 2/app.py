from dotenv import load_dotenv
import os
import streamlit as st
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import google.generativeai as genai

load_dotenv()

# Configure Google Gemini API key
genai.configure(api_key='AIzaSyB0PSskpLJ9UkLywPQGP-CydZPgBA8WHyw')

# Load the trained LSTM model for temperature prediction
model = load_model('temperature_predictions_model.h5')

# Load and fit the scaler (use the same scaler used during training)
df = pd.read_excel('B:/capstone project 2/city_temperature.xlsx')
chennai_df = df[df['City'] == 'Chennai (Madras)']
filtered_df = chennai_df[(chennai_df['AvgTemperature'] > 0) & (chennai_df['AvgTemperature'] <= 120)]

# Assuming that the scaler was trained on the 'AvgTemperature' column
scaler = MinMaxScaler()
scaler.fit(filtered_df[['AvgTemperature']])

# Prepare data for prediction
def prepare_data(date):
    # Convert date_input to pandas Timestamp
    date = pd.Timestamp(date)
    
    # Ensure the DataFrame index is a DateTimeIndex
    if not isinstance(filtered_df.index, pd.DatetimeIndex):
        filtered_df.index = pd.to_datetime(filtered_df.index)
    
    # Filter data up to the given date
    recent_data = filtered_df[filtered_df.index <= date]
    
    # Check if there is enough data to create a sequence
    if len(recent_data) < 10:
        st.error("Not enough data for the given date.")
        return None
    
    # Select the last 10 entries as the input sequence for prediction
    sequence = recent_data[['AvgTemperature']].tail(10).values
    
    # Normalize the data
    sequence = scaler.transform(sequence)
    
    return sequence

def predict_temperature(input_sequence):
    input_sequence = np.expand_dims(input_sequence, axis=0)  # Reshape for LSTM input
    prediction = model.predict(input_sequence)
    
    # Inverse transform the prediction
    predicted_temp = scaler.inverse_transform(np.repeat(prediction, input_sequence.shape[2], axis=-1))[:, 0]
    return predicted_temp[0]

# Function to get a response from Google Gemini
def get_gemini_response(question):
    prompt = f"""
    You are an expert in interpreting weather data and temperature predictions. Given the following query related to Chennai's temperature, provide detailed insights or answers.

    Examples of queries:
    - "What is the forecasted temperature for Chennai on December 25, 2024?"
    - "Predict the average temperature for the next week."
    - "What are the temperature trends in Chennai over the past decade?"

    Query: {question}
    """
    
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt])
    return response.text

# Streamlit app configuration
st.set_page_config(page_title="Temperature Prediction with Gemini")
st.header("Temperature Prediction Using LSTM Model and Gemini")

# User input for text query
user_query = st.text_input("Enter your question about the temperature (e.g., 'What will be the temperature next week?')")

submit = st.button("Get Temperature Prediction")

# If submit is clicked
if submit:
    # Generate a response using Google Gemini to interpret the query
    gemini_response = get_gemini_response(user_query)
    
    # Display the Gemini response
    st.subheader("Google Gemini Response")
    st.write(gemini_response)
    
    # Example: Handle specific types of predictions based on the interpreted query
    if "next week" in user_query.lower():
        # Prepare the data for the prediction of the next week (assuming the user wants the average temperature)
        # You can change the date to reflect the current date or a specified date
        date_input = pd.Timestamp.now()
        input_sequence = prepare_data(date_input)
        
        if input_sequence is not None:
            # Predict the temperature
            prediction = predict_temperature(input_sequence)
            st.subheader("Temperature Prediction")
            st.write(f"The predicted temperature for the next week is: {prediction:.2f}°F")
        else:
            st.error("Insufficient data to make a prediction for the next week.")
        
    elif "temperature on" in user_query.lower():
        # Extract the date from the query using Gemini's response
        # This is a placeholder; actual implementation would depend on the LLM's output
        date_input = pd.Timestamp('2024-09-17') 
        input_sequence = prepare_data(date_input)
        
        if input_sequence is not None:
            # Predict the temperature
            prediction = predict_temperature(input_sequence)
            st.subheader("Temperature Prediction")
            st.write(f"The predicted temperature for {date_input.date()} is: {prediction:.2f}°F")
        else:
            st.error(f"Insufficient data to make a prediction for {date_input.date()}.")
        
 


