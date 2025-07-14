import streamlit as st
import pandas as pd

st.title("Product Filter, Clean, and Group App")

st.markdown("""
Upload a CSV file. The app will:
- Filter products where:
  - RPM ≤ 0.001
  - Gross Revenue ≤ 1 USD
  - Gross Revenue is not blank
- Clean the Date field to only show date (remove time)
- Move **Campaign ID** to the first column
- Sort output by **Campaign ID ascending**
- Provide a downloadable filtered CSV.
""")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, sep=None, engine='python')

    st.subheader("Original Data Preview")
    st.dataframe(df.head())

    # Ensure required columns exist
    required_cols = {'RPM', 'Gross Revenue', 'Campaign ID', 'Date'}
    if required_cols.issubset(df.columns):
        # Remove rows where Gross Revenue is blank or NaN
        df = df[df['Gross Revenue'].notna()]

        # Filter by RPM and Gross Revenue
        filtered_df = df[(df['RPM'] <= 0.001) & (df['Gross Revenue'] <= 1)]

        # Clean Date column: remove time part
        filtered_df['Date'] = pd.to_datetime(filtered_df['Date']).dt.date

        # Move Campaign ID to the first column
        cols = filtered_df.columns.tolist()
        cols.remove('Campaign ID')
        cols = ['Campaign ID'] + cols
        filtered_df = filtered_df[cols]

        # Sort by Campaign ID ascending
        filtered_df = filtered_df.sort_values(by='Campaign ID', ascending=True)

        st.subheader("Filtered, Cleaned, and Sorted Data Preview")
        st.dataframe(filtered_df)

        # Prepare CSV for download
        def convert_df_to_csv(df):
            return df.to_csv(index=False).encode('utf-8')

        csv = convert_df_to_csv(filtered_df)

        st.download_button(
            label="Download filtered CSV",
            data=csv,
            file_name='filtered_grouped_data.csv',
            mime='text/csv',
        )
    else:
        st.error(f"The uploaded file must contain the following columns: {', '.join(required_cols)}")
else:
    st.info("Please upload a CSV file to begin.")
