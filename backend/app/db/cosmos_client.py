from azure.cosmos.aio import CosmosClient
from azure.cosmos.exceptions import CosmosResourceNotFoundError


class CosmosDBClient:
    CONTAINER = "user-data"

    def __init__(self, endpoint: str, key: str, database_name: str) -> None:
        self._client = CosmosClient(endpoint, credential=key)
        self._database_name = database_name

    async def _container(self):
        database = self._client.get_database_client(self._database_name)
        return database.get_container_client(self.CONTAINER)

    async def get_user_config(self, user_id: str) -> dict | None:
        try:
            container = await self._container()
            return await container.read_item(item=f"{user_id}-config", partition_key=user_id)
        except CosmosResourceNotFoundError:
            return None
        except Exception as exc:
            raise RuntimeError(f"Error leyendo configuración de {user_id}: {exc}") from exc

    async def save_user_config(self, user_id: str, config: dict) -> dict:
        try:
            container = await self._container()
            document = {**config, "id": f"{user_id}-config", "user_id": user_id}
            return await container.upsert_item(document)
        except Exception as exc:
            raise RuntimeError(f"Error guardando configuración de {user_id}: {exc}") from exc

    async def get_macro_plan(self, user_id: str) -> dict | None:
        try:
            container = await self._container()
            return await container.read_item(item=f"{user_id}-macro-plan", partition_key=user_id)
        except CosmosResourceNotFoundError:
            return None
        except Exception as exc:
            raise RuntimeError(f"Error leyendo plan macro de {user_id}: {exc}") from exc

    async def save_macro_plan(self, user_id: str, plan: dict) -> dict:
        try:
            container = await self._container()
            document = {**plan, "id": f"{user_id}-macro-plan", "user_id": user_id}
            return await container.upsert_item(document)
        except Exception as exc:
            raise RuntimeError(f"Error guardando plan macro de {user_id}: {exc}") from exc

    async def close(self) -> None:
        await self._client.close()
