import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from PIL import Image
import requests
from io import BytesIO
from utility import submit_data,firebase_data_loader2

def image_faridabad(df):
    st.header("Property Remarks")
    property_id = st.text_input("Enter Property ID:", key=12798)
    name = st.text_input("Enter Name:", key=12645)
    remarks = st.text_input("Enter Remarks:", key=12908)
    if st.button("Submit", key=12646):
        submit_data(property_id, name, remarks)
    if st.button("Show remarks", key=12647):
        df1 = firebase_data_loader2()
        st.dataframe(df1)

    df['Date'] = df['Date'].dt.tz_convert('Asia/Kolkata')
    col1, col2, col3 = st.columns((3))

    startDate = pd.to_datetime(datetime.today() - timedelta(days=1))
    endDate = pd.to_datetime(datetime.today())

    with col1:
        st.markdown('<p style="font-size:22px; color:blue; font-weight:bold;">Select Date</p>', unsafe_allow_html=True)
    with col2:
        date1 = pd.to_datetime(st.date_input("Start Date", startDate, key=12999))
    with col3:
        date2 = pd.to_datetime(st.date_input("End Date", endDate, key=12000))

    date1 = date1.replace(hour=23, minute=59, second=15).tz_localize('UTC').tz_convert('Asia/Kolkata')
    date2 = pd.to_datetime(date2).tz_localize('UTC').tz_convert('Asia/Kolkata')
    date2 = date2 + timedelta(hours=23, minutes=59)

    df = df[(df['Date'] > date1) & (df['Date'] <= date2)]

    search_property_id = st.text_input("Search by Property ID", key=1343)
    if search_property_id:
        st.subheader("Images")
        display_images(df, search_property_id)
    else:
        st.subheader("Images")
        display_images(df)

@st.cache_data
def display_images(df, search_property_id=None):
    placeholder_image_path = "images.png"

    for index, row in df.iterrows():
        property_id = row['Property_ID']
        receiver_image_url = row['receiver_image']
        property_image_url = row['property_image']

        if search_property_id and search_property_id.lower() not in property_id.lower():
            continue

        col1, col2 = st.columns(2)

        with col1:
            display_image(property_id, receiver_image_url, placeholder_image_path)
        with col2:
            display_image(property_id, property_image_url, placeholder_image_path)

def display_image(property_id, image_url, placeholder_image_path):
    if not image_url:
        image = Image.open(placeholder_image_path)
        st.image(image, caption=f"{property_id}", width=150)
        return

    response = requests.get(image_url)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        st.image(image, caption=property_id, width=150)
    else:
        placeholder_image = Image.open(placeholder_image_path)
        st.image(placeholder_image, caption=f"{property_id}", width=150)
