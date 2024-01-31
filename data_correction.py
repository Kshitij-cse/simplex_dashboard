import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import os
import pandas as pd
def data_correction(df):

    uploaded_file = st.sidebar.file_uploader("Choose an Excel file", type=["xls", "xlsx"])
    if uploaded_file is not None:
        st.sidebar.success("File uploaded successfully!")
        df1 = pd.read_excel(uploaded_file)

        merged_df = pd.merge(df1, df, on='Property_ID', how='left', suffixes=('_df1', '_df'))
        for column in ['District', 'Colony', 'Vendor', 'Date', 'Phone']:
            df1[column] = merged_df[f'{column}_df18'].combine_first(merged_df[f'{column}_df1'])

        db = firestore.client()

        data_to_upload = df1.to_dict(orient='records')
        for data in data_to_upload:
            doc_ref, doc_id = db.collection("Dashboard_Testing").add(data)
            print(f"Document added with ID: {doc_id}")