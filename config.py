import os

# ----------------------------------------------------------------
# Configuración de conexión a Neo4j
# Ajusta las variables de entorno o modifica los valores por defecto
# ----------------------------------------------------------------
NEO4J_URI      = os.getenv("NEO4J_URI",      "bolt://localhost:7687")
NEO4J_USER     = os.getenv("NEO4J_USER",     "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "12345678")
