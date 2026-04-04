import streamlit as st
import pandas as pd
from controllers.database.database import db
from controllers.database.encuesta import get_encuesta_entry_with_reference
from controllers.database.const import COD_PROYECTO
from controllers.database.data_base import get_productores_schema

import streamlit as st
import pandas as pd

def render_seccion_dinamica(diccionario_seccion, nombre_llave):
    st.write(f"### {nombre_llave.replace('_', ' ').upper()}")
    
    # 1. CASO TABLA: Si es un diccionario de diccionarios (Población)
    primer_valor = next(iter(diccionario_seccion.values()))
    if isinstance(primer_valor, dict) and not any(isinstance(v, bool) for v in primer_valor.values()):
        df = pd.DataFrame.from_dict(diccionario_seccion, orient='index')
        edited_df = st.data_editor(df, width='stretch', key=f"editor_{nombre_llave}")
        return edited_df.to_dict(orient='index')
    
    # 2. CASO MIXTO/SIMPLE: (Manejo Sanitario, Reproducción, etc.)
    else:
        for campo, valor in diccionario_seccion.items():
            # Si detectamos el sub-corchete (ej: vacunacion)
            if isinstance(valor, dict):
                st.markdown(f"**Sub-sección: {campo.replace('_', ' ').capitalize()}**")
                # Iteramos los hijos de esa sub-sección AQUÍ MISMO
                for sub_campo, sub_valor in valor.items():
                    key_ui = f"w_{nombre_llave}_{campo}_{sub_campo}"
                    # Dibujamos el widget directamente
                    if isinstance(sub_valor, bool):
                        diccionario_seccion[campo][sub_campo] = st.checkbox(f"{sub_campo}", value=sub_valor, key=key_ui)
                    # (Puedes agregar más tipos como number_input si el PDF lo requiere)
            
            # Si es un campo simple fuera de sub-corchetes
            else:
                key_ui = f"w_{nombre_llave}_{campo}"
                if isinstance(valor, bool):
                    diccionario_seccion[campo] = st.checkbox(f"{campo}", value=valor, key=key_ui)
                elif isinstance(valor, (int, float)):
                    diccionario_seccion[campo] = st.number_input(f"{campo}", value=valor, key=key_ui)
                else:
                    diccionario_seccion[campo] = st.text_input(f"{campo}", value=str(valor), key=key_ui)
                    
        return diccionario_seccion


# Configuración de UI
st.set_page_config(page_title="Sistema de Encuestas ", layout="wide")

st.title("📋 Ficha de Caracterización Pecuaria")
st.caption(f"Proyecto Oficial: {COD_PROYECTO}") # 

with st.expander("👤 1. Identificación del Productor", expanded=True):
    datos_encuesta = get_productores_schema()
    
    with st.form("form_productor"):
        st.subheader("Datos Básicos")
        
        dni = st.text_input("Ingrese DNI del Productor", max_chars=8, help="Debe tener 8 dígitos")
        
        st.divider()
        
        for seccion, contenido in datos_encuesta.items():
            datos_encuesta[seccion] = render_seccion_dinamica(contenido, seccion)
        
        btn_validar = st.form_submit_button("Validar y Continuar")
        
        if btn_validar:
            if len(dni) == 8:
                # Guardamos el DNI en el esquema
                datos_encuesta["productor"]["dni"] = dni
                st.success(f"✅ Productor {dni} listo para la ficha técnica.")
                # Aquí podrías usar st.session_state para guardar este progreso
            else:
                st.error("❌ El DNI debe tener exactamente 8 caracteres.")
# --- PASO 2: Selección de Tipo de Ficha ---
tipo_ficha = st.sidebar.selectbox(
    "Seleccione el Tipo de Ficha",
    ["VACUNO", "PORCINO"] # 
)

if dni:
    datos_encuesta = get_encuesta_entry_with_reference(dni, tipo_ficha)
    
    st.subheader(f"Formulario Técnico: {tipo_ficha}")
    
    with st.form("form_tecnico"):

        st.subheader(f"Formulario: {tipo_ficha}")
        
        for seccion, contenido in datos_encuesta.items():
            
            if seccion == "metadatos":
                continue 
            
            datos_encuesta[seccion] = render_seccion_dinamica(contenido, seccion)
            st.divider()  

        btn_guardar = st.form_submit_button("Finalizar y Guardar en Firebase")
        
        # En app.py, antes de guardar:
        if btn_guardar:
            key_pob = "poblacion_ganadera" if tipo_ficha == "VACUNO" else "poblacion_porcina"
            for categoria in datos_encuesta[key_pob]:
                valores = datos_encuesta[key_pob][categoria]
                suma = sum(v for k, v in valores.items() if k != "total")
                datos_encuesta[key_pob][categoria]["total"] = suma

            if datos_encuesta:
                db.collection("encuestas").add(datos_encuesta)
                st.success("✅ ¡Guardado!")
            else:
                st.error("❌ El esquema de la encuesta está vacío.")
else:
    st.warning("⚠️ Ingrese un DNI para comenzar la encuesta.")