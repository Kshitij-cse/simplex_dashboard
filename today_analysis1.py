import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from utility import  generate_grouped_df, gen_csv,create_download_buttons,select_columns

def today_analysis1(df):
    col1, col2, col3 = st.columns((3))
    date1 = pd.to_datetime(datetime.today() - timedelta(days=1))
    date1 = date1.replace(hour=23, minute=59, second=15)
    date2 = pd.to_datetime(datetime.now())
    df = df[(df['Date'] > date1.tz_localize(None)) & (df['Date'] <= date2.tz_localize(None))]

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
        csv5,pdf_buffer5= gen_csv(result5,'Colonies wise')
        create_download_buttons(pdf_buffer5,csv5,68,98)

    df = select_columns(df)
    csv6,pdf_buffer6= gen_csv(df,'Raw Data')
    create_download_buttons(pdf_buffer6,csv6,700,701)      