import pandas as pd
import streamlit as st
from utility import generate_grouped_df, gen_csv,create_download_buttons,select_columns_faridabad
from datetime import datetime, timedelta
def historical_analysis_faridabad(df):
    col1, col2, col3 = st.columns((3))

    df['Date'] = df['Date'].dt.tz_convert('Asia/Kolkata')
    startDate = df["Date"].min()
    endDate = pd.to_datetime(datetime.today())
    
    with col1:
        st.markdown('<p style="font-size:22px; color:blue; font-weight:bold;">Historical Analysis</p>', unsafe_allow_html=True)
    with col2:
        date1 = pd.to_datetime(st.date_input("Start Date", startDate))
    with col3:
        date2 = pd.to_datetime(st.date_input("End Date", endDate,key=2222))
    
    date1 = pd.to_datetime(date1).tz_localize('UTC').tz_convert('Asia/Kolkata')
    date2 = pd.to_datetime(date2).tz_localize('UTC').tz_convert('Asia/Kolkata')
    date2 = date2 + timedelta(hours=23,minutes=59)

    df = df[(df['Date'] >= date1) & (df['Date'] <= date2)]
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    df.rename(columns={'district': 'MC'}, inplace=True)

    result4 = generate_grouped_df(df[['Property_ID','Surveyor number', 'Colony']], ['Surveyor number', 'Colony'])
    result5 = generate_grouped_df(df[['Property_ID', 'Colony']], ['Colony'])

    total_properties_covered = df.shape[0]
    col8, col9 = st.columns((2))
    with col8:
        csv4,pdf_buffer4= gen_csv(result4,(f" {'Surveyor no wise:'} {total_properties_covered}"))
        create_download_buttons(pdf_buffer4,csv4,2169,2199)

    with col9:
        csv5,pdf_buffer5= gen_csv(result5,'Colonies wise:')
        create_download_buttons(pdf_buffer5,csv5,2170,21100)
    df = select_columns_faridabad(df)
    
    csv6,pdf_buffer6= gen_csv(df,'Raw Data')
    create_download_buttons(pdf_buffer6,csv6,21705,21706)