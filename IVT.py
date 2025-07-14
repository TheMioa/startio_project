import streamlit as st
import pandas as pd

st.title("IVT % Checker")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.write("### Preview of uploaded data")
    st.dataframe(df.head())

    # Ensure correct column name
    if 'Advertiser' in df.columns and 'IVT (%)' in df.columns:
        result_df = df.copy()
        flags = []

        # Compute quartiles for each Advertiser
        quartiles = df.groupby('Advertiser')['IVT (%)'].quantile([0.5, 0.75]).unstack()

        # Iterate rows to flag conditions
        for idx, row in df.iterrows():
            adv = row['Advertiser']
            ivt = row['IVT (%)']
            median_ivt = quartiles.loc[adv, 0.5]
            q3_ivt = quartiles.loc[adv, 0.75]

            if ivt > q3_ivt:
                flag = "Critical High IVT"
            elif ivt > median_ivt:
                flag = "Warning High IVT"
            else:
                flag = "OK"
            flags.append(flag)

        result_df['IVT Flag'] = flags

        st.write("### IVT Flag Results")
        st.dataframe(result_df[['Advertiser', 'IVT (%)', 'IVT Flag']])

        st.download_button(
            label="Download results as CSV",
            data=result_df.to_csv(index=False).encode('utf-8'),
            file_name="ivt_flag_results.csv",
            mime="text/csv"
        )
    else:
        st.error("CSV must contain 'Advertiser' and 'IVT (%)' columns.")
