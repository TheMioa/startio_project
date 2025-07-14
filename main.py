import streamlit as st
import pandas as pd

st.title("Product Filter, Clean, Group and Column Management App")

st.markdown("""
Upload a CSV file. The app will:
- Filter products where:
  - RPM > 0.001
  - Gross Revenue > 1 USD
  - Gross Revenue is not blank
- Clean Date to show only date (no time)
- Optional triggers to remove columns before grouping:
  - Remove **Package** and **Product**
  - Remove **Date**
- Group results by **Campaign ID** after column removal
- Move **Campaign ID** to first column
- Sort by **Campaign ID ascending**
- Provide downloadable filtered CSV.
""")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, sep=None, engine='python')

    st.subheader("Original Data Preview")
    st.dataframe(df.head())

    required_cols = {'RPM', 'Gross Revenue', 'Campaign ID', 'Date'}
    if required_cols.issubset(df.columns):
        df = df[df['Gross Revenue'].notna()]
        filtered_df = df[(df['RPM'] > 0.001) & (df['Gross Revenue'] > 1)].copy()

        filtered_df['Date'] = pd.to_datetime(filtered_df['Date']).dt.date

        st.subheader("Configure Output Columns")

        remove_package_product = st.checkbox("Remove 'Package' and 'Product' columns")
        if remove_package_product:
            cols_to_remove = [col for col in ['Package', 'Product'] if col in filtered_df.columns]
            filtered_df = filtered_df.drop(columns=cols_to_remove)
            st.info(f"Removed columns: {', '.join(cols_to_remove)}")

        remove_date = st.checkbox("Remove 'Date' column")
        if remove_date and 'Date' in filtered_df.columns:
            filtered_df = filtered_df.drop(columns=['Date'])
            st.info("Removed column: Date")

        # Group by Campaign ID and aggregate numeric columns
        numeric_cols = filtered_df.select_dtypes(include='number').columns.tolist()
        group_cols = ['Campaign ID']
        agg_dict = {col: 'sum' for col in numeric_cols if col != 'Campaign ID'}

        grouped_df = filtered_df.groupby('Campaign ID', as_index=False).agg(agg_dict)

        # Optionally keep one value for non-numeric columns (first occurrence)
        non_numeric_cols = [col for col in filtered_df.columns if col not in numeric_cols + ['Campaign ID']]
        for col in non_numeric_cols:
            first_values = filtered_df.groupby('Campaign ID')[col].first().reset_index()
            grouped_df = pd.merge(grouped_df, first_values, on='Campaign ID', how='left')

        # Move Campaign ID to first column
        cols = grouped_df.columns.tolist()
        cols.remove('Campaign ID')
        cols = ['Campaign ID'] + cols
        grouped_df = grouped_df[cols]

        # Sort by Campaign ID ascending
        grouped_df = grouped_df.sort_values(by='Campaign ID', ascending=True)

        st.subheader("Filtered, Cleaned, Grouped and Sorted Data Preview")
        st.dataframe(grouped_df)

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
        st.error(f"The uploaded file must contain columns: {', '.join(required_cols)}")
else:
    st.info("Please upload a CSV file to begin.")
