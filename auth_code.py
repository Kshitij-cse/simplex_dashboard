from pathlib import Path
import pickle
import streamlit_authenticator as stauth
import streamlit as st
import yaml
from yaml.loader import SafeLoader


def auth_code():
    file_path = Path(__file__).parent / "hashed_pw.pkl"
    cred_path = Path(__file__).parent / "cred.yaml"

    with file_path.open("rb") as file:
        hashed_passwords = pickle.load(file)

    with cred_path.open('rb') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    name, authentication_status, username = authenticator.login("main")

    # if "authentication_status" not in st.session_state:
    #  st.session_state.authentication_status = authentication_status
    # if not authentication_status:
    #     st.error("Username/password is incorrect")
    # if authentication_status is None:
    #     st.warning("Enter username and password")
    
    
    
    if st.session_state["authentication_status"]:
        st.write(f'Welcome *{st.session_state["name"]}*')
        st.title('Some content')
    elif st.session_state["authentication_status"] == False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] == None:
        st.warning('Please enter your username and password')
    return authentication_status, username, authenticator