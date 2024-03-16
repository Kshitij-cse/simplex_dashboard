import pandas as pd
import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from datetime import datetime, timedelta
def Image_tab(df):
    if st.button("Show Historical Images"):
        
        search_property_id = st.text_input("Search by Property ID")

        for index, row in df.iterrows():
            property_id = row['Property_ID']
            image_url = row['property_image']
            
            if search_property_id and search_property_id.lower() not in property_id.lower():
                continue
            
            response = requests.get(image_url)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                st.image(image, caption=property_id, width=150)
            else:
                st.write(f"Failed to retrieve image for property ID: {property_id}")

        if not search_property_id:
            st.header("All Images")
            for index, row in df.iterrows():
                property_id = row['Property_ID']
                image_url = row['property_image']
                response = requests.get(image_url)
                if response.status_code == 200:
                    image = Image.open(BytesIO(response.content))
                    st.image(image, caption=property_id, width=150)
                else:
                    st.write(f"Failed to retrieve image for property ID: {property_id}")

        date1 = pd.to_datetime(datetime.today() - timedelta(days=1))
        date1 = date1.replace(hour=23, minute=59, second=15)
        date2 = pd.to_datetime(datetime.now())
        df = df[(df['Date'] > date1.tz_localize(None)) & (df['Date'] <= date2.tz_localize(None))]            

    if st.button("Show Today Images"):
        
        search_property_id = st.text_input("Search by Property ID")

        for index, row in df.iterrows():
            property_id = row['Property_ID']
            image_url = row['property_image']
            
            if search_property_id and search_property_id.lower() not in property_id.lower():
                continue
            
            response = requests.get(image_url)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                st.image(image, caption=property_id, width=150)
            else:
                st.write(f"Failed to retrieve image for property ID: {property_id}")

        if not search_property_id:
            st.header("All Images")
            for index, row in df.iterrows():
                property_id = row['Property_ID']
                image_url = row['property_image']
                response = requests.get(image_url)
                if response.status_code == 200:
                    image = Image.open(BytesIO(response.content))
                    st.image(image, caption=property_id, width=150)
                else:
                    st.write(f"Failed to retrieve image for property ID: {property_id}")