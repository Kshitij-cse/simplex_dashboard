import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from PIL import Image
import requests
from io import BytesIO
from utility import submit_data,firebase_data_loader2
def Image_tab(df):

    st.header("Property Remarks")
    property_id = st.text_input("Enter Property ID:",key=798)
    name = st.text_input("Enter Name:",key=645)
    remarks = st.text_input("Enter Remarks:",key=908)
    if st.button("Submit",key=646):
        submit_data(property_id, name, remarks)
    if st.button("Show remarks",key=647):
        df1 = firebase_data_loader2() 
        st.dataframe(df1) 

    date1 = pd.to_datetime(datetime.today() - timedelta(days=1))
    date1 = date1.replace(hour=23, minute=59, second=15)
    date2 = pd.to_datetime(datetime.now())
    df = df[(df['Date'] > date1.tz_localize(None)) & (df['Date'] <= date2.tz_localize(None))]
    
    search_property_id = st.text_input("Search by Property ID")
    col1, col2 = st.columns(2)
    if search_property_id:
        with col1:
            display_images(df, search_property_id, 'property_image')
        with col2:
            display_images(df, search_property_id, 'receiver_image')
    else:
        with col1:
            st.subheader("Property Images")
            display_images(df, column='property_image')
        with col2:
            st.subheader("Receiver Images")
            display_images(df, column='receiver_image')

@st.cache_data
def display_images(df, search_property_id=None, column=None):
    placeholder_image_path = "images.png"  

    for index, row in df.iterrows():
        property_id = row['Property_ID']
        image_url = row[column]

        if not image_url:
            image = Image.open(placeholder_image_path)
            st.image(image, caption=f" {property_id}", width=150)
            continue

        if search_property_id and search_property_id.lower() not in property_id.lower():
            continue

        response = requests.get(image_url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            st.image(image, caption=property_id, width=150)
        else:
            placeholder_image = Image.open(placeholder_image_path)
            st.image(placeholder_image, caption=f" {property_id}", width=150)
