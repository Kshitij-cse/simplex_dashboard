import streamlit as st
import warnings
import pandas as pd
from auth_code import auth_code
from images_tab import Image_tab
from today_analysis import today_analysis
from historicaL_analysis import historical_analysis
from today_analysis1 import today_analysis1
from historical_analysis1 import historical_analysis1
from utility import firebase_data_loader,firebase_data_loader1,firebase_data_loaderfb,firebase_data_loaderfb1,firebase_data_loaderonlyfb,fetch_faridabad_include_submitted
import streamlit_authenticator as stauth
from analytics_page import  Analytics_tab
from today_faridabad import today_analysis_faridabad
from historical_faridabad import historical_analysis_faridabad
from images_faridabad import image_faridabad
import time
from const import cols_to_be_removed
st.set_page_config(page_title="Simplex Dashboard", page_icon=":bar_chart:", layout="wide")
warnings.filterwarnings('ignore')

st.title(" :bar_chart: Simplex Dashboard")
authentication_status, username, authenticator = auth_code()
if authentication_status: 
    def clear_cache():
     st.cache_data.clear()

    st.sidebar.button("Refresh",on_click=clear_cache)
    authenticator.logout("Logout", "sidebar",key=17)
    tab_titles = ["Today Faridabad","Historical Faridabad","Faridabad Images"]
    tabs = st.tabs(tab_titles)
    st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
    
    # df = firebase_data_loader()
    # df1 = firebase_data_loader1()
    # df = pd.merge(df1, df[['vendor_name', '_8_digit_UPID']], on='_8_digit_UPID', how='left')
    
    # df["district"] = df["district"].str.lower()
    # df['modifiedAtString'] = pd.to_datetime(df['modifiedAtString'], unit='ms')
    
    # df.rename(columns={'vmc_colony_name': 'Colony'}, inplace=True)
    # df.rename(columns={'vendor_name': 'Vendor'}, inplace=True)
    # df.rename(columns={'userPhoneNumber': 'Phone'}, inplace=True)
    # df.rename(columns={'_8_digit_UPID': 'Property_ID'}, inplace=True)
    # df.rename(columns={'modifiedAtString':'Date'}, inplace=True)
    # df.rename(columns={'mobileNumberOfOwner':'Mobile'}, inplace=True)
     
    #10 colony data
    #df1 = firebase_data_loaderfb()
    #faridabad single node
    #df1.to_excel('data1.xlsx')
    #df2 = firebase_data_loaderonlyfb()
    #df2.to_excel('data2.xlsx')
   
    #fbdf = pd.concat([df1, df2], ignore_index=True)
    #df1,df2 = None,None

    df3= firebase_data_loaderfb1()
    #df3.to_excel("data3.xlsx")
    df4 = fetch_faridabad_include_submitted()
   
    fbdf = pd.concat([df3, df4], ignore_index=True)

    df3,df4 = None,None

    #fbdf = pd.merge(fbdf1, fbdf[['_8_digit_UPID','image']], on='_8_digit_UPID', how='left')
    

    fbdf['modifiedAtString'] = pd.to_datetime(fbdf['modifiedAtString'], unit='ms')
    fbdf['modifiedAtString'] = fbdf['modifiedAtString'].dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata')

    fbdf.rename(columns={'vmc_colony_name': 'Colony'}, inplace=True)
    fbdf.rename(columns={'vendor_name': 'Vendor'}, inplace=True)
    fbdf.rename(columns={'userPhoneNumber': 'Surveyor number'}, inplace=True)
    fbdf.rename(columns={'_8_digit_UPID': 'Property_ID'}, inplace=True)
    fbdf.rename(columns={'modifiedAtString':'Date'}, inplace=True)
    fbdf.rename(columns={'mobileNumberOfOwner':'Mobile'}, inplace=True)
    
    st.sidebar.header("Choose your filter: ")

    colony_list = st.sidebar.multiselect("Pick the Colony", fbdf["Colony"].unique())
    if colony_list:
        fbdf = fbdf[fbdf["Colony"].isin(colony_list)]
    user_list = st.sidebar.multiselect("Select Surveyor number", fbdf["Surveyor number"].unique(),default=[])

    if user_list :
        fbdf = fbdf[fbdf["Surveyor number"].isin(user_list)]
    
    
    # if(username=="master"):
        # with tabs[0]:
        #     today_analysis(df)
        # with tabs[1]:
        #     historical_analysis(df)
        # with tabs[2]:
        #      Analytics_tab(df)   
        # with tabs[3]:
        #      Image_tab(df)
        # with tabs[0]:
        #      today_analysis_faridabad(fbdf)
        # with tabs[1]:
        #      historical_analysis_faridabad(fbdf)    
        # with tabs[2]:
        #      image_faridabad(fbdf)
                   
    if(username=='faridabad'):
        with tabs[0]:
            today_analysis_faridabad(fbdf)
        with tabs[1]:
            historical_analysis_faridabad(fbdf)
        with tabs[2]:
                image_faridabad(fbdf)
#3elif(username=='assandh'):
        # with tabs[0]:
        #     today_analysis1(df)
        # with tabs[1]:
        #     historical_analysis1(df)
         