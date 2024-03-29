import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from utility import df_to_pdf
from utility import df_to_pdf, generate_grouped_df, gen_csv,create_download_buttons,send_email,select_columns
def historical_analysis(df):
    col1, col2, col3 = st.columns((3))
   
    startDate = df["Date"].min()
    endDate = pd.to_datetime(datetime.today())
    
    with col1:
        st.markdown('<p style="font-size:22px; color:blue; font-weight:bold;">Historical Analysis</p>', unsafe_allow_html=True)
    with col2:
        date1 = pd.to_datetime(st.date_input("Start Date", startDate))
    with col3:
        date2 = pd.to_datetime(st.date_input("End Date", endDate))
    
    date1 = pd.to_datetime(date1)
    date2 = pd.to_datetime(date2)
    date2 = date2 + timedelta(hours=23,minutes=59)
    df = df[(df['Date'] >= date1) & (df['Date'] <= date2)]

    df.rename(columns={'district': 'MC'}, inplace=True)
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
        create_download_buttons(pdf_buffer,csv,71,81)

    with col5:
        csv1,pdf_buffer1 = gen_csv(result1, 'MC/Colony:')
        create_download_buttons(pdf_buffer1, csv1,72,82)

    col6, col7 = st.columns((2))
    with col6:
       
        csv2,pdf_buffer2=gen_csv(result2,'Vendor/Colony:')
        create_download_buttons(pdf_buffer2,csv2,73,83)

    with col7:
        csv3,pdf_buffer3 = gen_csv(result3,'Colony/Vendor:')
        create_download_buttons(pdf_buffer3,csv3,74,84)

    col8, col9 = st.columns((2))

    with col8:
        csv4,pdf_buffer4= gen_csv(result4,'Phone no wise:')
        create_download_buttons(pdf_buffer4,csv4,75,85)

    with col9:
        csv5,pdf_buffer5= gen_csv(result5,'Colonies wise:')
        create_download_buttons(pdf_buffer5,csv5,76,86)

    df = select_columns(df)    
    csv6,pdf_buffer6= gen_csv(df,'Raw Data')
    create_download_buttons(pdf_buffer6,csv6,805,806)

    st.header("Enter emails to send data")
    
    rec_email = []
    emails_input = st.text_input("Enter Emails (separated by commas) and then press enter:", "",key=567)
    if st.button("Click to Send Data",key=21):
        if emails_input: 
            emails = [email.strip() for email in emails_input.split(",") if email.strip()]  
            rec_email.extend(emails)
            st.success(f"Sent data to {len(emails)} email(s)")
            send_email( rec_email,result4)
        else:
            st.warning("Please enter valid emails.")
    
        