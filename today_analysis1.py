import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from utility import  generate_grouped_df, gen_csv,create_download_buttons

def today_analysis1(df):
    col1, col2, col3 = st.columns((3))
    df["Date"] = pd.to_datetime(df["Date"])

    date1 = pd.to_datetime(datetime.now() - timedelta(days=20))
    date2 = pd.to_datetime('today')
    #date1 = pd.Timestamp(date1, tz="UTC")
    #date2 = pd.Timestamp(date2, tz="UTC")
    
    df = df[(df["Date"] >= date1) & (df["Date"] <= date2)]

    with col1:
        st.markdown('<p style="font-size:22px; color:blue; font-weight:bold;">Today Analysis</p>',
                    unsafe_allow_html=True)
   
    result4 = generate_grouped_df(df, ['Phone', 'Colony'])
    result5 = generate_grouped_df(df, ['Colony'])
    total_properties_covered = df.shape[0]
    col8, col9 = st.columns((2))

    with col8:
        csv4,pdf_buffer4= gen_csv(result4,(f" {'Phone no wise:'} {total_properties_covered}"))
        create_download_buttons(pdf_buffer4,csv4,67,97)

    with col9:
        csv5,pdf_buffer5= gen_csv(result5,'Colonies wise:')
        create_download_buttons(pdf_buffer5,csv5,68,98)