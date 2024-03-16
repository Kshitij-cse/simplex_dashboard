import pandas as pd
import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from utility import days_fetcher,target_fetcher,store_days,store_target,Upload_Data,create_download_buttons,gen_csv1,select_columns,submit_data,firebase_data_loader2
def Analytics_tab(df):
    df.rename(columns={'district': 'MC'}, inplace=True)
    df = select_columns(df) 
    total_properties_covered = df.shape[0]
    set_target = target_fetcher()
    no_of_days= days_fetcher()
    col1, col2 = st.columns((2))
    with col1:
        user_input_target = st.number_input("Set property target:",step=1)   
            
    with col2:
        col1, col2 = st.columns((2))

        with col1:
            date1 = st.date_input("Start Date")
        with col2:
            date2 = st.date_input("End Date")
        
        user_input_days = (date2 - date1).days  
        user_input_days = st.number_input("Set no of days:", step=1, value=user_input_days)  
        if st.button("Click to update",key=333):
            if(user_input_target==0):
                st.error("Property target is empty")
            elif(user_input_days==0):
                st.error("No. of Days is empty")    
            else:
                store_days(user_input_days)
                store_target(user_input_target)
                st.success("Updated Succesfully")

    properties_left = set_target-total_properties_covered
    perday_prop = properties_left/no_of_days
    col1, col2, col3 = st.columns(3) 
    with col1:
        st.markdown(f"<h3 style='color: blue;'>Target: {int(set_target)}</h4>", unsafe_allow_html=True)
    with col2: 
        st.markdown(f"<h3 style='color: blue;'>Properties left: {int(properties_left)}</h3>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<h3 style='color: blue;'>Per/day target: {int(perday_prop)}</h3>", unsafe_allow_html=True)
    
    st.header('Search Property')
    search_criteria = st.selectbox('Search by:', ['Property_ID', 'Vendor', 'Mobile'])
    search_query = st.text_input(f'Enter {search_criteria}:')
    
    if search_query:
        # Filtering based on user input
        if search_criteria == 'Property_ID':
            filtered_data = df.query(f'Property_ID == {search_query}')
        elif search_criteria == 'Vendor':
            filtered_data = df.query(f'Vendor.str.contains("{search_query}", case=False)')
        elif search_criteria == 'Mobile':
            filtered_data = df.query(f'Mobile == "{search_query}"')
        st.dataframe(filtered_data)
        csv,pdf_buffer =gen_csv1(filtered_data)
        create_download_buttons(pdf_buffer,csv,300,400)

    st.header("Update Data with CSV/Excel")
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1]
        if file_extension == "csv":
            df = pd.read_csv(uploaded_file)
        elif file_extension == "xlsx":
            df = pd.read_excel(uploaded_file, engine='openpyxl')
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
            return
        Upload_Data(df)
        st.success("Uploaded Succesfully")
        st.write("Preview of the DataFrame:")
        st.write(df)
    
    st.header("Property Remarks")

    property_id = st.text_input("Enter Property ID:")
    name = st.text_input("Enter Name:")
    remarks = st.text_input("Enter Remarks:")

    if st.button("Submit"):
        submit_data(property_id, name, remarks)
      

    if st.button("Show remarks"):
        df1 = firebase_data_loader2() 
        st.dataframe(df1) 