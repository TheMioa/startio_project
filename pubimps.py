import streamlit as st
import pandas as pd
import numpy as np

st.title("Discrepancy Checker: Publisher vs Advertiser Impressions")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully.")
    
    # Ensure numeric types
    df['Publisher Impressions'] = pd.to_numeric(df['Publisher Impressions'], errors='coerce')
    df['Advertiser Impressions'] = pd.to_numeric(df['Advertiser Impressions'], errors='coerce')
    
    # Calculate discrepancy
    df['Discrepancy'] = np.abs(df['Publisher Impressions'] - df['Advertiser Impressions']) / df['Publisher Impressions']
    
    # Flag rows where discrepancy > 20%
    threshold = 0.20
    flagged_df = df[df['Discrepancy'] > threshold]
    
    st.subheader(f"Flagged rows (Discrepancy > {int(threshold*100)}%)")
    st.dataframe(flagged_df)
    
    # Allow download
    csv = flagged_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download flagged rows as CSV",
        data=csv,
        file_name='flagged_discrepancies.csv',
        mime='text/csv',
    )
else:
    st.info("Awaiting file upload.")

