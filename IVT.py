import streamlit as st
import pandas as pd

st.title("IVT % Checker with Quartile Flags")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.write("### Preview of uploaded data")
    st.dataframe(df.head())

    # Check that necessary columns exist
    if 'Advertiser' in df.columns and 'IVT (%)' in df.columns:
        # Compute median and Q3 for each Advertiser
        quartiles = df.groupby('Advertiser')['IVT (%)'].quantile([0.5, 0.75]).unstack()

        # Function to determine flag
        def flag_ivt(row):
            adv = row['Advertiser']
            ivt = row['IVT (%)']
            median_ivt = quartiles.loc[adv, 0.5]
            q3_ivt = quartiles.loc[adv, 0.75]
            if ivt > q3_ivt:
                return "Critical High IVT"
            elif ivt > median_ivt:
                return "Warning High IVT"
            else:
                return "OK"

        # Apply flagging
        df['IVT Flag'] = df.apply(flag_ivt, axis=1)

        st.write("### Data with IVT Flag")
        st.dataframe(df)

        st.download_button(
            label="Download updated file as CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name="ivt_flagged.csv",
            mime="text/csv"
        )
    else:
        st.error("CSV must contain 'Advertiser' and 'IVT (%)' columns.")
