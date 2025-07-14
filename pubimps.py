import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Impression Discrepancy Checker")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully.")
    
    # Ensure numeric types
    df['Publisher Impressions'] = pd.to_numeric(df['Publisher Impressions'], errors='coerce')
    df['Advertiser Impressions'] = pd.to_numeric(df['Advertiser Impressions'], errors='coerce')
    
    # Avoid division by zero
    df = df[df['Advertiser Impressions'] > 0]
    
    # Calculate discrepancy: 1 - (PubImp / AdvImp)
    df['Discrepancy'] = 1 - (df['Publisher Impressions'] / df['Advertiser Impressions'])
    
    st.subheader("Discrepancy Distribution")
    # Plot histogram with 5% bins
    fig, ax = plt.subplots()
    bins = np.arange(-1, 1.05, 0.05)  # From -100% to +100% in 5% increments
    ax.hist(df['Discrepancy'], bins=bins, edgecolor='black')
    ax.set_xlabel('Discrepancy (1 - PubImp/AdvImp)')
    ax.set_ylabel('Count')
    ax.set_title('Distribution of Impression Discrepancies')
    st.pyplot(fig)
    
    # User toggles
    st.subheader("Flagged rows")
    show_under = st.checkbox("Show Under-delivery (>10%)", value=True)
    show_over = st.checkbox("Show Over-delivery (<-10%)", value=True)
    
    flagged_df = pd.DataFrame()
    
    if show_under and show_over:
        flagged_df = df[(df['Discrepancy'] > 0.10) | (df['Discrepancy'] < -0.10)]
    elif show_under:
        flagged_df = df[df['Discrepancy'] > 0.10]
    elif show_over:
        flagged_df = df[df['Discrepancy'] < -0.10]
    
    st.dataframe(flagged_df)
    
    # Download button
    if not flagged_df.empty:
        csv = flagged_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download flagged rows as CSV",
            data=csv,
            file_name='flagged_discrepancies.csv',
            mime='text/csv',
        )
else:
    st.info("Awaiting file upload.")
