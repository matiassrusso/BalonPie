# balonpie-api

Backend FastAPI de BalonPie. Expone datos de futbol argentino consumidos desde API-Football y normalizados para el frontend.

## Endpoints

- `/health`
- `/proximos-partidos`
- `/ultima-fecha`
- `/tabla`
- `/equipos`
- `/equipo/{nombre}`
- `/partido/{fixture_id}`

## Desarrollo local

1. Instalar dependencias: `pip install -r requirements.txt`
2. Completar `API_FOOTBALL_KEY` en `.env`
3. Levantar el servidor: `uvicorn main:app --reload`

Base URL local: `http://127.0.0.1:8000`

## Tests

Ejecutar:

```bash
pytest
```

## Notas del estado actual

- El proyecto esta centrado en la temporada 2024 por limitaciones del plan Free de API-Football.
- `/proximos-partidos` hoy funciona como navegacion historica por fecha dentro de 2024.
- El seed de equipos todavia necesita ampliarse con `scripts/fetch_teams.py`.
