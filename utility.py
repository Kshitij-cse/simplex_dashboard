from PIL import Image
import requests
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import os
import pandas as pd
from google.api_core.retry import Retry
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
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

def gen_csv1(df):
    pdf_buffer = df_to_pdf(df)
    return df.to_csv(index=False).encode('utf-8'),pdf_buffer

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
@st.cache_data
def firebase_data_loader():
    if not firebase_admin._apps:
      cred = credentials.Certificate("firebase-credentials.json")
      firebase_admin.initialize_app(cred)

    db = firestore.client()
    collection_name = "assandh" 
    docs = db.collection(collection_name).stream(retry=Retry())
    data_list = []
    for doc in docs:
        data_list.append(doc.to_dict())
    df = pd.DataFrame(data_list)
    return df
@st.cache_data
def firebase_data_loader1():
    if not firebase_admin._apps:
      cred = credentials.Certificate("firebase-credentials.json")
      firebase_admin.initialize_app(cred)

    db = firestore.client()
    collection_name = "assandhSubmitted" 
    docs = db.collection(collection_name).stream(retry=Retry())
    data_list = []
    for doc in docs:
        data_list.append(doc.to_dict())
    df = pd.DataFrame(data_list)
    return df

@st.cache_data
def firebase_data_loader2():
    if not firebase_admin._apps:
      cred = credentials.Certificate("firebase-credentials.json")
      firebase_admin.initialize_app(cred)

    db = firestore.client()
    collection_name = "property_remarks" 
    docs = db.collection(collection_name).stream(retry=Retry())
    data_list = []
    for doc in docs:
        data_list.append(doc.to_dict())
    df = pd.DataFrame(data_list)
    df['submission_date'] = pd.to_datetime(df['submission_date']).dt.date
    
    return df

def Upload_Full():
    df =pd.read_excel('haryana7.xlsx')
    db = firestore.client()
    data_dict = df.to_dict(orient='records')
    for i, record in enumerate(data_dict):
        doc_ref = db.collection("Uploaded_Data").document(f'doc_{i}')
        doc_ref.set(record)
    
def run():
 
    db = firestore.client()
    doc_ref = db.collection('integers').document('day')
    doc_ref.set({'Days': 30})
    doc_ref = db.collection('integers').document('Property')
    doc_ref.set({'Target': 3000})
   
def days_fetcher():
    db = firestore.client()
    doc_ref = db.collection('integers').document('day')
    doc = doc_ref.get()
    days_data = doc.to_dict()
    days_value = days_data.get('Days')
    return days_value

def target_fetcher():
    db = firestore.client()
    doc_ref = db.collection('integers').document('Property')
    doc = doc_ref.get()
    days_data = doc.to_dict()
    days_value = days_data.get('Target')
    return days_value
    
def store_days(new_value):

    db = firestore.client()
    doc_ref = db.collection("integers").document('day')
    doc_ref.update({'Days': new_value})

def store_target(new_value):

    db = firestore.client()
    doc_ref = db.collection("integers").document('Property')
    doc_ref.update({'Target': new_value})
       
def Upload_Data(df):
    db = firestore.client()
   
    for index, row in df.iterrows():
        Property_ID = row['Property_ID']
        query = db.collection('Dashboard_Testing').where('Property_ID', '==', Property_ID)
        docs = query.stream()

        for doc in docs:
            doc.reference.update({
                'Phone': row['Phone'],
                'Vendor': row['Vendor'],
                'Colony': row['Colony'],
                'District': row['District'],
                'Property_ID': row['Property_ID'],
                'Date': row['Date'],
                
            })


def uploader():
   
    df = pd.read_excel("colony.xlsx")
    colony_names = df["Colony Name"].tolist()
    db = firestore.client()
    key_name = "assandh"
    data = {key_name: colony_names}
    document_id = "assandh"
    doc_ref = db.collection('districtwithcolonies').document(document_id)
    doc_ref.set(data)

def send_email( receiver_emails,dataframe):
    sender_email = "murfiprop@gmail.com"
    sender_password = "lvri pmyn iiwj bygn"
    subject = "Property Data"
    body = "Please find the attached CSV file."

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = ', '.join(receiver_emails)
    message['Subject'] = subject
    
    csv_data = dataframe.to_csv(index=False)

    message.attach(MIMEText(body, 'plain'))

    # Attach CSV data to the email
    part = MIMEBase('text', 'csv')
    part.set_payload(csv_data.encode())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={subject}.csv')
    message.attach(part)

    # Connect to SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)

    # Send email to each recipient
    for receiver_email in receiver_emails:
        # Update the receiver email in the message
        message.replace_header('To', receiver_email)
        # Send email
        server.sendmail(sender_email, receiver_email, message.as_string())

    server.quit()

def select_columns(df):

    selected_columns = ['Date', 'Property_ID', 'distributionPossible', 'owner_name', 'whatsapp_number', 'Mobile', 'Phone', 'property_type', 'property_image', 'receiver_image', 'image', 'property_category', 'postal_address', 'plot_area', 'Colony', 'signature', 'reason', 'receiver_name', 'property_usage', 'latitude', 'longitude', 'ownerFatherOrHusbandName', 'total_carpet_area', 'Vendor', 'MC', 'water_bill_consumer_id', 'nonSubmittable', 'old_Tax_d','landmark']
   
    df_filtered = df[selected_columns]
   
    df_filtered = df_filtered.reset_index(drop=True)
    
    return df_filtered

def submit_data(property_id, name, remarks):
    if property_id and name and remarks:  
        db = firestore.client()
        submission_date = datetime.now()
        data = {
            "property_id": property_id,
            "name": name,
            "remarks": remarks,
            "submission_date": submission_date
        }
        db.collection("property_remarks").add(data)
        st.success("Data submitted successfully!")
    else:
        st.error("Please fill in all fields.")



        