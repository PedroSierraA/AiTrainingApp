import httpx

BASE_URL = "https://intervals.icu/api/v1"


class ICUClient:
    """Cliente para la API pública de intervals.icu.

    Nota: intervals.icu NO expone un endpoint separado de "fitness".
    CTL/ATL se leen del endpoint de wellness (icu_ctl, icu_atl) y
    TSB se calcula como CTL - ATL.
    """

    def __init__(self, api_key: str) -> None:
        self._client = httpx.AsyncClient(
            base_url=BASE_URL,
            auth=httpx.BasicAuth("API_KEY", api_key),
            timeout=30.0,
        )

    async def get_athlete(self, athlete_id: str) -> dict:
        try:
            response = await self._client.get(f"/athlete/{athlete_id}/profile")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as exc:
            raise RuntimeError(f"Error obteniendo perfil del atleta {athlete_id}: {exc}") from exc

    async def get_fitness(self, athlete_id: str, oldest: str, newest: str) -> dict:
        try:
            response = await self._client.get(
                f"/athlete/{athlete_id}/wellness",
                params={"oldest": oldest, "newest": newest},
            )
            response.raise_for_status()
            days = response.json()
            if not days:
                return {}
            latest = days[-1]
            ctl = latest.get("ctl", latest.get("icu_ctl"))
            atl = latest.get("atl", latest.get("icu_atl"))
            return {
                "date": latest.get("id"),
                "ctl": ctl,
                "atl": atl,
                "tsb": (ctl - atl) if ctl is not None and atl is not None else None,
                "history": days,
            }
        except httpx.HTTPError as exc:
            raise RuntimeError(f"Error obteniendo fitness de {athlete_id}: {exc}") from exc

    async def get_wellness(self, athlete_id: str, date: str) -> dict:
        try:
            response = await self._client.get(f"/athlete/{athlete_id}/wellness/{date}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as exc:
            raise RuntimeError(f"Error obteniendo wellness de {athlete_id} en {date}: {exc}") from exc

    async def get_activities(self, athlete_id: str, oldest: str, newest: str) -> list:
        try:
            response = await self._client.get(
                f"/athlete/{athlete_id}/activities",
                params={"oldest": oldest, "newest": newest},
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as exc:
            raise RuntimeError(f"Error obteniendo actividades de {athlete_id}: {exc}") from exc

    async def get_activity(self, athlete_id: str, activity_id: str) -> dict:
        try:
            response = await self._client.get(f"/activity/{activity_id}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as exc:
            raise RuntimeError(f"Error obteniendo actividad {activity_id}: {exc}") from exc

    async def get_activity_power_curve(self, athlete_id: str, activity_id: str) -> dict:
        try:
            response = await self._client.get(f"/activity/{activity_id}/power-curve.json")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as exc:
            raise RuntimeError(
                f"Error obteniendo curva de potencia de la actividad {activity_id}: {exc}"
            ) from exc

    async def push_workout(self, athlete_id: str, workout_data: dict) -> dict:
        try:
            response = await self._client.post(
                f"/athlete/{athlete_id}/events/bulk",
                params={"upsert": "true"},
                json=[workout_data],
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as exc:
            raise RuntimeError(f"Error subiendo workout para {athlete_id}: {exc}") from exc

    async def close(self) -> None:
        await self._client.aclose()
