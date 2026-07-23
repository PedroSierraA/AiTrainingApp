from fastapi import APIRouter

router = APIRouter(prefix="/config", tags=["config"])

# Endpoints pendientes: leer/guardar configuración del atleta en Cosmos DB.
