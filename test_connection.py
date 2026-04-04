from controllers.database.database import db

try:
    # Intentamos obtener las colecciones (aunque esté vacía, debe responder)
    collections = db.collections()
    print("¡Conexión exitosa! [Success]")
    print(f"Colecciones disponibles: {[c.id for c in collections]}")
except Exception as e:
    print("Error de conexión [Failure]")
    print(f"Detalle del error: {e}")