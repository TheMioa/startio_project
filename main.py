import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Product Filter and Grouping App")

st.markdown("""
Upload a CSV file. The app will:
- Filter products where:
  - RPM ≤ 0.001
  - Gross Revenue ≤ 1 USD
  - Gross Revenue is not blank
- Group the results by **Campaign ID**
- Provide a downloadable filtered CSV.
""")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, sep=None, engine='python')

    st.subheader("Original Data Preview")
    st.dataframe(df.head())

    # Ensure required columns exist
    required_cols = {'RPM', 'Gross Revenue', 'Campaign ID'}
    if required_cols.issubset(df.columns):
        # Remove rows where Gross Revenue is blank or NaN
        df = df[df['Gross Revenue'].notna()]

        # Filter by RPM and Gross Revenue
        filtered_df = df[(df['RPM'] <= 0.001) & (df['Gross Revenue'] <= 1)]

        # Group by Campaign ID (simply for organization, not aggregation)
        grouped_df = filtered_df.groupby('Campaign ID').apply(lambda x: x).reset_index(drop=True)

        st.subheader("Filtered and Grouped Data Preview")
        st.dataframe(grouped_df)

        # Prepare CSV for download
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
        st.error(f"The uploaded file must contain the following columns: {', '.join(required_cols)}")
else:
    st.info("Please upload a CSV file to begin.")
