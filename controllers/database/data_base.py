def get_productores_schema():
    return {
        "productor": {
            "apellido_paterno": "",
            "apellido_materno": "",
            "nombres": "",
            "dni": "",
            "celular": "",
            "grado_instruccion": "", # [cite: 6]
            "integrantes_familia": 0, # [cite: 7]
            "asistencia_tecnica": False, # [cite: 8]
            "capacitacion": False # [cite: 9]
        },
        "ubicacion": {
            "region": "",
            "provincia": "",
            "distrito": "",
            "localidad": "",
            "coordenadas": {
                "latitud": 0.0,
                "longitud": 0.0,
                "altitud": 0 # [cite: 11]
            }
        },
}