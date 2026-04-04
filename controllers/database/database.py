import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

def connect_db():
    if not firebase_admin._apps:
        try:
            key_dict = st.secrets["textkey"] 
            cred = credentials.Certificate(dict(key_dict))
        except Exception:
            cred = credentials.Certificate("key.json")
            
        firebase_admin.initialize_app(cred)
    
    return firestore.client()

db = connect_db()