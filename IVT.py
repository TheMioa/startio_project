import streamlit as st
import pandas as pd

st.title("IVT % Checker with Quartile Flags and Summary Table")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.write("### Preview of uploaded data")
    st.dataframe(df.head())

    # Check required columns
    if 'Advertiser' in df.columns and 'IVT (%)' in df.columns:
        # Compute quartiles
        quartiles = df.groupby('Advertiser')['IVT (%)'].quantile([0.65, 0.8]).unstack()
        quartiles.columns = ['0.65', '0.8']
        quartiles = quartiles.reset_index()

        # Show quartile summary table for verification
        st.write("### Quartile Summary per Advertiser")
        st.dataframe(quartiles)

        # Create lookup dict for fast row-wise checking
        quartile_dict = quartiles.set_index('Advertiser').to_dict('index')

        # Function to flag IVT
        def flag_ivt(row):
            adv = row['Advertiser']
            ivt = row['IVT (%)']
            median_ivt = quartile_dict[adv]['0.65']
            q3_ivt = quartile_dict[adv]['0.8']
            if ivt > q3_ivt:
                return "Critical High IVT"
            elif ivt > median_ivt:
                return "Warning High IVT"
            else:
                return "OK"

        # Apply flagging
        df['IVT Flag'] = df.apply(flag_ivt, axis=1)

        # Show data with new column
        st.write("### Data with IVT Flag")
        st.dataframe(df)

        # Allow download
        st.download_button(
            label="Download updated file as CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name="ivt_flagged.csv",
            mime="text/csv"
        )
    else:
        st.error("CSV must contain 'Advertiser' and 'IVT (%)' columns.")
