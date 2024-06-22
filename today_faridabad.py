import pandas as pd
import pytz
import streamlit as st
from datetime import datetime, timedelta, timezone
from utility import  generate_grouped_df, gen_csv,create_download_buttons,select_columns,select_columns_faridabad

def today_analysis_faridabad(df):
    
    col1, col2, col3 = st.columns((3))

    
    df['Date'] = df['Date'].dt.tz_convert('Asia/Kolkata')
    date1 = datetime.now(tz=pytz.timezone('Asia/Kolkata')) - timedelta(days=1)
    date1 = date1.replace(hour=23, minute=59, second=15)
    date2 = datetime.now(tz=pytz.timezone('Asia/Kolkata'))
    df = df[(df['Date'] > date1) & (df['Date'] <= date2)]
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')

    with col1:
        st.markdown('<p style="font-size:22px; color:blue; font-weight:bold;">Today Analysis</p>',
                    unsafe_allow_html=True)
    df.rename(columns={'district': 'MC'}, inplace=True)
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

    df = select_columns_faridabad(df)
    
    csv6,pdf_buffer6= gen_csv(df,'Raw Data')
    create_download_buttons(pdf_buffer6,csv6,700,701)