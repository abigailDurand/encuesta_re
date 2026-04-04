import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import os

def connect_db():
    if not firebase_admin._apps:
        # 1. INTENTO: ¿Estamos en Streamlit Cloud?
        try:
            if "textkey" in st.secrets:
                secret_dict = dict(st.secrets["textkey"])
                # Sanitización de la llave para la nube
                if "private_key" in secret_dict:
                    secret_dict["private_key"] = secret_dict["private_key"].replace("\\n", "\n")
                cred = credentials.Certificate(secret_dict)
                firebase_admin.initialize_app(cred)
                return firestore.client()
        except Exception:
            # Si falla el acceso a secrets, simplemente pasamos al siguiente método
            pass

        # 2. INTENTO: ¿Estamos en Local? (Buscamos el archivo físico)
        if os.path.exists("key.json"):
            cred = credentials.Certificate("key.json")
            firebase_admin.initialize_app(cred)
            return firestore.client()
        else:
            st.error("❌ No se encontró la configuración de Firebase (ni Secrets ni key.json)")
            return None
    
    return firestore.client()

db = connect_db()