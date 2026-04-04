
# Importamos las funciones desde sus respectivos archivos
from controllers.database.estructura_vacuno import get_vacuno_schema
from controllers.database.estructura_porcino import get_porcino_schema
from controllers.database.data_base import get_productores_schema
def get_encuesta_entry_with_reference(dni_productor, tipo_encuesta):
    base_productor = get_productores_schema()
    # Solo generamos el esquema que  necesitamos
    if tipo_encuesta == "VACUNO":
        schema_tecnico = get_vacuno_schema()
    elif tipo_encuesta == "PORCINO":
        schema_tecnico = get_porcino_schema()
    else:
        raise ValueError("Tipo de encuesta no reconocido") # [cite: 36, 43]
    
    schema = base_productor | schema_tecnico 
    schema["productor"]["dni"] = dni_productor
    schema["metadatos"]["tipo_unidad"] = tipo_encuesta # [cite: 36]
    
    return schema