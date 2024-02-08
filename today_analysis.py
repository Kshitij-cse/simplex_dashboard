import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from utility import  generate_grouped_df, gen_csv,create_download_buttons


def today_analysis(df):
    col1, col2, col3 = st.columns((3))
    df["Date"] = pd.to_datetime(df["Date"])

    date1 = pd.to_datetime(datetime.now() - timedelta(days=20))
    date2 = pd.to_datetime('today')
    date1 = pd.Timestamp(date1, tz="UTC")
    date2 = pd.Timestamp(date2, tz="UTC")
    
    df = df[(df["Date"] >= date1) & (df["Date"] <= date2)]
    df.rename(columns={'District': 'MC'}, inplace=True)
    with col1:
        st.markdown('<p style="font-size:22px; color:blue; font-weight:bold;">Today Analysis</p>',
                    unsafe_allow_html=True)

    result = generate_grouped_df(df, ['MC', 'Vendor'])
    total_properties_covered = df.shape[0]
    result1 = generate_grouped_df(df, ['MC', 'Colony'])
    result2 = generate_grouped_df(df, ['Vendor', 'Colony'])
    result3 = generate_grouped_df(df, ['Colony', 'Vendor'])
    result4 = generate_grouped_df(df, ['Vendor', 'Phone', 'Colony'])
    result5 = generate_grouped_df(df, ['Colony'])
    
    col4, col5 = st.columns((2))
    with col4:
        csv,pdf_buffer = gen_csv(result,(f" {'Total Property'} {total_properties_covered}"))
        create_download_buttons(pdf_buffer,csv,61,91)

    with col5:
        csv1,pdf_buffer1 = gen_csv(result1, 'MC/Colony:')
        create_download_buttons(pdf_buffer1, csv1,62,92)

    col6, col7 = st.columns((2))
    with col6:
        csv2,pdf_buffer2=gen_csv(result2,'Vendor/Colony:')
        create_download_buttons(pdf_buffer2,csv2,63,93)

    with col7:
        csv3,pdf_buffer3 = gen_csv(result3,'Colony/Vendor:')
        create_download_buttons(pdf_buffer3,csv3,64,94)

    col8, col9 = st.columns((2))

    with col8:
        csv4,pdf_buffer4= gen_csv(result4,'Phone no wise:')
        create_download_buttons(pdf_buffer4,csv4,65,95)

    with col9:
        csv5,pdf_buffer5= gen_csv(result5,'Colonies wise:')
        create_download_buttons(pdf_buffer5,csv5,66,96)
