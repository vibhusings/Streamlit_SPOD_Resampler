import streamlit as st
import pandas as pd
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def resample_to_hourly(data):
    try:
        data['Local Date Time'] = pd.to_datetime(data['Local Date Time'], format='%m/%d/%Y %I:%M:%S %p')
        data.set_index('Local Date Time', inplace=True)
        
        # Select only numeric columns
        numeric_cols = data.select_dtypes(include='number').columns
        data_numeric = data[numeric_cols]
        
        # Resample and compute mean
        hourly_data = data_numeric.resample('h').mean()
        
        return hourly_data
    except Exception as e:
        st.error(f"Error processing the file: {e}")
        return None

# Streamlit UI
st.title("SPOD Minute to Hourly Resampler")
st.write("Upload a CSV file to resample its data to an hourly frequency.")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.write("### Preview of Uploaded Data:")
        st.dataframe(df.head())
        
        processed_data = resample_to_hourly(df)
        
        if processed_data is not None:
            st.write("### Hourly Resampled Data:")
            st.dataframe(processed_data.head())
            
            # Provide a download link
            csv = processed_data.to_csv().encode('utf-8')
            st.download_button(
                label="Download Hourly Resampled CSV",
                data=csv,
                file_name="hourly_resampled.csv",
                mime="text/csv"
            )
    except Exception as e:
        st.error(f"Failed to process the file: {e}")
