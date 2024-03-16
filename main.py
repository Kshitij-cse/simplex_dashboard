import streamlit as st
import warnings
import pandas as pd
from auth_code import auth_code
from images_tab import Image_tab
from today_analysis import today_analysis
from historicaL_analysis import historical_analysis
from today_analysis1 import today_analysis1
from historical_analysis1 import historical_analysis1
from utility import firebase_data_loader,firebase_data_loader1
import streamlit_authenticator as stauth
from analytics_page import  Analytics_tab
import time
st.set_page_config(page_title="Simplex Dashboard", page_icon=":bar_chart:", layout="wide")
warnings.filterwarnings('ignore')

st.title(" :bar_chart: Simplex Dashboard")
authentication_status, username, authenticator = auth_code()


if authentication_status: 
    authenticator.logout("Logout", "sidebar",key=17)
    if(username== 'master'):
     tab_titles = ["Today Analysis", "Historical Analysis","Analytics","Property Images"]
    else:
     tab_titles = ["Today Analysis", "Historical Analysis"] 
    tabs = st.tabs(tab_titles)
    st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

    df = firebase_data_loader()
    df1 = firebase_data_loader1()
    df = pd.merge(df1, df[['vendor_name', '_8_digit_UPID']], on='_8_digit_UPID', how='left')
    
    df["district"] = df["district"].str.lower()
    df['modifiedAtString'] = pd.to_datetime(df['modifiedAtString'], unit='ms')
    
    df.rename(columns={'vmc_colony_name': 'Colony'}, inplace=True)
    df.rename(columns={'vendor_name': 'Vendor'}, inplace=True)
    df.rename(columns={'userPhoneNumber': 'Phone'}, inplace=True)
    df.rename(columns={'_8_digit_UPID': 'Property_ID'}, inplace=True)
    df.rename(columns={'modifiedAtString':'Date'}, inplace=True)
    df.rename(columns={'mobileNumberOfOwner':'Mobile'}, inplace=True)

    if username.lower() != "master":
        df = df[df["district"] == username.lower()]

    st.sidebar.header("Choose your filter: ")
    if(username=="master"):
     district_list = st.sidebar.multiselect("Pick your District", df["district"].unique())
     if district_list:
        df = df[df["district"].isin(district_list)]
    colony_list = st.sidebar.multiselect("Pick the Colony", df["Colony"].unique())
    if colony_list:
        df = df[df["Colony"].isin(colony_list)]
    if(username=="master"):
     vendor_list = st.sidebar.multiselect("Pick the Vendor", df["Vendor"].unique())
     if vendor_list:
        df = df[df["Vendor"].isin(vendor_list)]
    
    if(username=="master"):
        with tabs[0]:
            today_analysis(df)
        with tabs[1]:
            historical_analysis(df)
        with tabs[2]:
             Analytics_tab(df)   
        with tabs[3]:
             Image_tab(df)
    else:
        with tabs[0]:
            today_analysis1(df)
        with tabs[1]:
            historical_analysis1(df)
         