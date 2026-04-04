import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

def connect_db():
    if not firebase_admin._apps:
        try:
            if "textkey" in st.secrets:
                secret_dict = dict(st.secrets["textkey"])
                cred = credentials.Certificate(secret_dict)
            else:
                cred = credentials.Certificate("key.json")
        except Exception as e:
            st.error(f"Error de configuración de Firebase: {e}")
            raise e
            
        firebase_admin.initialize_app(cred)
    
    return firestore.client()

db = connect_db()