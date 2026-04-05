import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from controllers.database.database import db
from controllers.database.encuesta import get_encuesta_entry_with_reference
from controllers.database.const import COD_PROYECTO
from controllers.database.data_base import get_productores_schema




def render_seccion_dinamica(diccionario_seccion, nombre_llave, contexto="main"):
    st.write(f"### {nombre_llave.replace('_', ' ').upper()}")

    if not diccionario_seccion:
        st.info(f"Sección '{nombre_llave}' sin datos.")
        return diccionario_seccion

    # Verificamos si absolutamente todos los campos de esta sección son sub-diccionarios
    todos_son_diccionarios = all(isinstance(v, dict) for v in diccionario_seccion.values())

    if todos_son_diccionarios:
        primer_valor = next(iter(diccionario_seccion.values()))
        tiene_diccionarios_anidados = any(isinstance(v, dict) for v in primer_valor.values())
        if not tiene_diccionarios_anidados:
            df = pd.DataFrame.from_dict(diccionario_seccion, orient='index')
            edited_df = st.data_editor(df, width='stretch', key=f"editor_{contexto}_{nombre_llave}")
            return edited_df.to_dict(orient='index')

    for campo, valor in diccionario_seccion.items():
        if isinstance(valor, dict):
            st.markdown(f"**Sub-sección: {campo.replace('_', ' ').capitalize()}**")
            
            # Intentamos mostrar la sub-sección entera como una tabla de 1 fila
            tiene_sub_diccionarios = any(isinstance(v, dict) for v in valor.values())
            if not tiene_sub_diccionarios:
                df_sub = pd.DataFrame.from_dict({campo: valor}, orient='index')
                edited_df_sub = st.data_editor(df_sub, width='stretch', key=f"editor_{contexto}_{nombre_llave}_{campo}")
                diccionario_seccion[campo] = edited_df_sub.to_dict(orient='index')[campo]
                continue

            for sub_campo, sub_valor in valor.items():
                if isinstance(sub_valor, dict):
                    st.markdown(f"*{sub_campo.replace('_', ' ').capitalize()}*")
                    
                    # Si llegamos al 3er nivel, intentamos mostrarlo como tabla de 1 fila
                    tiene_sub_sub_diccionarios = any(isinstance(v, dict) for v in sub_valor.values())
                    if not tiene_sub_sub_diccionarios:
                        df_sub_sub = pd.DataFrame.from_dict({sub_campo: sub_valor}, orient='index')
                        edited_df_sub_sub = st.data_editor(df_sub_sub, width='stretch', key=f"editor_{contexto}_{nombre_llave}_{campo}_{sub_campo}")
                        diccionario_seccion[campo][sub_campo] = edited_df_sub_sub.to_dict(orient='index')[sub_campo]
                    else:
                        for sub_sub_campo, sub_sub_valor in sub_valor.items():
                            key_ui = f"w_{contexto}_{nombre_llave}_{campo}_{sub_campo}_{sub_sub_campo}"
                            if isinstance(sub_sub_valor, bool):
                                diccionario_seccion[campo][sub_campo][sub_sub_campo] = st.checkbox(f"{sub_sub_campo}", value=sub_sub_valor, key=key_ui)
                            elif isinstance(sub_sub_valor, (int, float)):
                                diccionario_seccion[campo][sub_campo][sub_sub_campo] = st.number_input(f"{sub_sub_campo}", value=sub_sub_valor, key=key_ui)
                            else:
                                diccionario_seccion[campo][sub_campo][sub_sub_campo] = st.text_input(f"{sub_sub_campo}", value=str(sub_sub_valor), key=key_ui)
                else:
                    key_ui = f"w_{contexto}_{nombre_llave}_{campo}_{sub_campo}"
                    if isinstance(sub_valor, bool):
                        diccionario_seccion[campo][sub_campo] = st.checkbox(f"{sub_campo}", value=sub_valor, key=key_ui)
                    elif isinstance(sub_valor, (int, float)):
                        diccionario_seccion[campo][sub_campo] = st.number_input(f"{sub_campo}", value=sub_valor, key=key_ui)
                    else:
                        diccionario_seccion[campo][sub_campo] = st.text_input(f"{sub_campo}", value=str(sub_valor), key=key_ui)
        else:
            key_ui = f"w_{contexto}_{nombre_llave}_{campo}"
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
    # Usamos session_state para que el DNI persista entre recargas
    if "dni_validado" not in st.session_state:
        st.session_state.dni_validado = None
    if "datos_productor" not in st.session_state:
        st.session_state.datos_productor = None

    datos_encuesta_prod = get_productores_schema()
    
    with st.form("form_productor"):
        st.subheader("Datos Básicos")
        dni_input = st.text_input("Ingrese DNI del Productor", max_chars=8, help="Debe tener 8 dígitos")
        
        st.divider()
        
        for seccion, contenido in datos_encuesta_prod.items():
            if seccion == "productor":
                copia_contenido = contenido.copy()
                if "dni" in copia_contenido:
                    del copia_contenido["dni"]
                datos_encuesta_prod[seccion] = render_seccion_dinamica(copia_contenido, seccion, contexto="productor")
            else:
                datos_encuesta_prod[seccion] = render_seccion_dinamica(contenido, seccion, contexto="productor")
        
        btn_validar = st.form_submit_button("Validar y Continuar")
        
        if btn_validar:
            if len(dni_input) == 8:
                st.session_state.dni_validado = dni_input
                st.session_state.datos_productor = datos_encuesta_prod.get("productor", {})
                st.success(f"✅ Productor {dni_input} validado localmente.")
            else:
                st.error("❌ El DNI debe tener 8 dígitos.")

tipo_ficha = st.sidebar.selectbox("Seleccione el Tipo de Ficha", ["VACUNO", "PORCINO"])

if st.session_state.dni_validado:
    dni_actual = st.session_state.dni_validado
    datos_tecnicos = get_encuesta_entry_with_reference(dni_actual, tipo_ficha)
    
    st.subheader(f"Formulario Técnico: {tipo_ficha}")
    
    with st.form("form_tecnico"):
        for seccion, contenido in datos_tecnicos.items():
            # Evitamos renderizar los metadatos y el productor que ya se llenó
            if seccion in ["metadatos", "productor"]:
                continue 
            datos_tecnicos[seccion] = render_seccion_dinamica(contenido, seccion, contexto="tecnico")
            st.divider()  

        btn_guardar = st.form_submit_button("Finalizar y Guardar en Firebase")
        
        if btn_guardar:
            # Restauramos los datos del productor que fueron validados en el paso 1
            if st.session_state.datos_productor:
                datos_tecnicos["productor"] = st.session_state.datos_productor
                datos_tecnicos["productor"]["dni"] = dni_actual

            # Lógica de cálculo de totales
            key_pob = "poblacion_ganadera" if tipo_ficha == "VACUNO" else "poblacion_porcino"
            for categoria in datos_tecnicos[key_pob]:
                valores = datos_tecnicos[key_pob][categoria]
                suma = sum(v for k, v in valores.items() if k != "total")
                datos_tecnicos[key_pob][categoria]["total"] = suma

            # Guardar en Firebase
            db.collection("encuestas").add(datos_tecnicos)
            st.success("✅ ¡Datos guardados exitosamente en Firebase!")
else:
    st.warning("⚠️ Valide el DNI en el Paso 1 para habilitar el formulario técnico.")