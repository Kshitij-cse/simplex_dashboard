from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import os
import pandas as pd

def df_to_pdf(df):
    buffer = BytesIO()

    pdf = SimpleDocTemplate(buffer, pagesize=letter)

    table_data = [df.columns.tolist()] + df.values.tolist()

    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), '#77AABB'),
                        ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1, 1)),
                        ('GRID', (0, 0), (-1, -1), 1, 'BLACK'),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

                        ])

    table = Table(table_data, style=style)
    pdf.build([table])
    buffer.seek(0)
    return buffer


def generate_grouped_df(df, col_list):
    return (df.groupby(col_list)['Property_ID'].nunique().reset_index()
            .rename(columns={'Property_ID': 'Properties Covered'}))


def gen_csv(df, name):
    st.subheader((f" {name} "))
    st.dataframe(df)
    pdf_buffer = df_to_pdf(df)
    return df.to_csv(index=False).encode('utf-8'),pdf_buffer

def create_download_buttons(pdf_buffer, csv_data,pdf_key,csv_key):
    col1, col2, col3 = st.columns(3)  

    with col1:
        st.download_button(label="Download PDF", data=pdf_buffer, file_name="dataframe.pdf",
                           mime="application/pdf", key=pdf_key)

    with col2:
        st.download_button(label="Download CSV", data=csv_data, file_name="Property.csv",
                           mime="text/csv", key=csv_key)

    with col3:
        st.write('')

def firebase_data_loader():
    if not firebase_admin._apps:
      cred = credentials.Certificate("firebase-credentials.json")
      firebase_admin.initialize_app(cred)

    db = firestore.client()
    collection_name = "Uploaded_Data" 
    docs = db.collection(collection_name).stream()
    data_list = []
    for doc in docs:
        data_list.append(doc.to_dict())
    df = pd.DataFrame(data_list)
    return df

