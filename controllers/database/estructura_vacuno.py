from controllers.database.const import COD_PROYECTO
PASTO_FORRAJE={
    "especies": "", "con_riego": False, "sin_riego": False, "total_ha": 0.0
}
INFRAESTRUCTURA={
    "cuenta": False, "estado_actual":{"bueno": False, "regular": False, "deficiente": False} 
    }
RAZAS_CATTLE = {
    "criollo": 0, "b_swiss": 0, "simental": 0, 
    "holstein": 0, "jersey": 0, "cebuino": 0, "total": 0
} 

RAZAS_LECHE = {
    "criolla": 0, "b_swiss": 0, "cebuino": 0, 
    "otros": 0, "total": 0
}
DESTINO_BASE = {
    "autoconsumo": 0, "mercado_local": 0, 
    "mercado_regional": 0, "total": 0
}
def get_vacuno_schema():
    return {
        "metadatos": {
            "tipo_unidad": "VACUNO", # [cite: 36]
            "proyecto_cui": COD_PROYECTO, # el encuestador pone
            "fecha_registro": "" 
        },
        
        "poblacion_ganadera": {
            "vacas_produccion": RAZAS_CATTLE.copy(),
            "vaquillonas": RAZAS_CATTLE.copy(),
            "terneras_1_6_meses": RAZAS_CATTLE.copy(),
            "terneras_7_12_meses": RAZAS_CATTLE.copy(),
            "vaquillas_13_18_meses": RAZAS_CATTLE.copy(),
            "terneros_1_6_meses": RAZAS_CATTLE.copy(),
            "terneros_7_12_meses": RAZAS_CATTLE.copy(),
            "toretes_mas_1_ano": RAZAS_CATTLE.copy(),
            "toros_mas_2_anos": RAZAS_CATTLE.copy(),
            "total": RAZAS_CATTLE.copy()

        },
        "reproduccion": {
            "monta_natural": False, # [cite: 12]
            "inseminacion_artificial": False, # [cite: 13]
            "ambos": False # [cite: 14]
        },
        "manejo_sanitario": {
            "vacunacion":{
                "rabia_bovina": False, 
                "carbuco_sint": False,
            },
            "desparasitacion": False,
            "suplementocion_minineral": False
        },
        "produccion_lechera": {
            "vacas_lecheras": RAZAS_LECHE.copy(),
            "rendimiento_vaca_dia": RAZAS_LECHE.copy(),
            "produccion_litro_dia": RAZAS_LECHE.copy(),
            "periodo_produccion_dias": RAZAS_LECHE.copy(),
            "produccion_campana": RAZAS_LECHE.copy(),
        },
        "destino_producion_anual":{
            "leche_fresca": DESTINO_BASE.copy(),
            "queso_fresco": DESTINO_BASE.copy(),
            "queso_maduro": DESTINO_BASE.copy(),
            "yogurt": DESTINO_BASE.copy(),
            "cachipa": DESTINO_BASE.copy(),
        },
        "disponibilidad_piso_forrajero": {
            "pasto_corte": PASTO_FORRAJE.copy(),
            "pasto_mejorado": PASTO_FORRAJE.copy(),
            "pasto_natural": PASTO_FORRAJE.copy(),
            "area_nueva_instalacion":PASTO_FORRAJE.copy(),
            "total": PASTO_FORRAJE.copy()
        },
        "infraestructura":{
            "cobertizo":INFRAESTRUCTURA.copy(),
            "corral": INFRAESTRUCTURA.copy(),
            "manga": INFRAESTRUCTURA.copy(),
            "cerco": INFRAESTRUCTURA.copy(),
            "pastizal_con_cerco": INFRAESTRUCTURA.copy()
        }
    }