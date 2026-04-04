from controllers.database.database import db
from firebase_admin import firestore

def seed_survey():
    # Referencia al documento (Usamos un DNI ficticio como ID)
    doc_ref = db.collection("encuestas_vacunos").document("00000000")

    # Estructura basada en el PDF
    data = {
        "productor": {
            "apellidos": "Prueba",
            "nombres": "Admin",
            "dni": "00000000"
        },
        "poblacion_ganadera": {
            "vacas_produccion": {"criollo": 5, "b_swiss": 10, "simental": 0, "total": 15}, # 
            "vaquillonas": {"criollo": 2, "b_swiss": 4, "simental": 1, "total": 7} # 
        },
        "produccion_lechera": {
            "rendimiento_vaca_dia": 10.5, # [cite: 19]
            "periodo_dias": 210, # [cite: 19]
            "total_campana": 2205.0 # (Rendimiento * Periodo)
        },
        "timestamp": firestore.SERVER_TIMESTAMP # Etiqueta de tiempo automática
    }

    doc_ref.set(data)
    print("¡Base de datos 'sembrada' con éxito!")

if __name__ == "__main__":
    seed_survey()