import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Product Filter and Grouping App")

st.markdown("""
This app allows you to upload a CSV file, filters products where:
- RPM ≤ 0.001
- Gross Revenue ≤ 1 USD

Then it groups the results by **Campaign ID** and provides a downloadable CSV.
""")

# File upload
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, sep=None, engine='python')  # auto-detect separator

    st.subheader("Original Data Preview")
    st.dataframe(df.head())

    # Ensure correct columns exist
    if {'RPM', 'Gross Revenue', 'Campaign ID'}.issubset(df.columns):
        # Filter condition
        filtered_df = df[(df['RPM'] <= 0.001) & (df['Gross Revenue'] <= 1)]

        # Group by Campaign ID
        grouped_df = filtered_df.groupby('Campaign ID').apply(lambda x: x).reset_index(drop=True)

        st.subheader("Filtered and Grouped Data Preview")
        st.dataframe(grouped_df)

        # Prepare downloadable file
        def convert_df_to_csv(df):
            return df.to_csv(index=False).encode('utf-8')

        csv = convert_df_to_csv(grouped_df)

        st.download_button(
            label="Download filtered CSV",
            data=csv,
            file_name='filtered_grouped_data.csv',
            mime='text/csv',
        )
    else:
        st.error("The uploaded file does not contain required columns: RPM, Gross Revenue, Campaign ID")
else:
    st.info("Please upload a CSV file to begin.")
