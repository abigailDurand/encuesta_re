from controllers.database.const import COD_PROYECTO
POBLACION_PORCINO = {
    "criollo": 0,
    "cruzados": 0,
    "Landrace": 0,
    "Yorshire": 0,
    "otros": 0,
    "total": 0
}


def get_porcino_schema():
    return {
        "metadatos": {
            "tipo_unidad": "PORCINO", 
            "proyecto_cui": COD_PROYECTO, 
            "fecha_registro": "" 
        },
        "poblacion_porcino": {
            "marranas_gestantes": POBLACION_PORCINO.copy(),
            "marranas_vacias": POBLACION_PORCINO.copy(),
            "gorrinas_remplazo": POBLACION_PORCINO.copy(),
            "lechones_lactantes": POBLACION_PORCINO.copy(),
            "lechones_destetados": POBLACION_PORCINO.copy(),
            "animales_recria_engorde": POBLACION_PORCINO.copy(),
            "verracos": POBLACION_PORCINO.copy(),
            "total": POBLACION_PORCINO.copy()
        },
        "infraestructura": {
            "traspatio": False, 
            "madera": False,
            "concreto": False,
        },
        "parametros": {
            "animales_reproducion":False,
            "tipo_de_enpadre": { "MN": False, "IA": False, "ambos": False },
            "atiende_partos": False,
            "lechones_por_parto_nacidos" : 0, 
            "lechones_por_parto_destetados": 0,
        },
        "tipo_alimentacion": {
            "balanceado": False,
            "residuo_de_cosina": False,
            "mixto": False,
            "restos_agroindustriales": False
        },
        "comercializacion": {
            "autoconsumo": False,
            "venta_en_pie": False,
            "venta_en_carne": False,
        }
    }