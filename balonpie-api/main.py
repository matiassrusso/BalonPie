import time

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

import api_football
import teams
from cache import CacheEntry, NoDataAvailableError, TTLCache

load_dotenv()

app = FastAPI(title="BalonPie API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

cache = TTLCache()

SEIS_HORAS = 6 * 3600
UNA_HORA = 3600
UN_MINUTO = 60
SEASON_MIN = 2022
SEASON_MAX = 2024
SEASON_DEFAULT = 2024


def _rango_fechas(season: int) -> tuple[str, str]:
    return f"{season}-01-01", f"{season}-12-31"


def _cached(key: str, ttl: float, fetch_fn, default):
    try:
        return cache.get_or_refresh(key, ttl, fetch_fn)
    except NoDataAvailableError:
        # No escribimos `default` en el cache: si quedara guardado ahí,
        # bloquearía reintentos hasta que venza el TTL completo aunque
        # API-Football se recupere al minuto siguiente.
        return CacheEntry(value=default, fetched_at=time.time(), is_stale=True)


def _live_snapshot() -> list[dict]:
    entry = _cached("live-snapshot", UN_MINUTO, lambda: api_football.get_live_snapshot(teams.COMPETICIONES), [])
    return entry.value


def _con_marcador_en_vivo(partidos: list[dict]) -> list[dict]:
    en_vivo_por_id = {p["id"]: p for p in _live_snapshot()}
    resultado = []
    for partido in partidos:
        vivo = en_vivo_por_id.get(partido["id"])
        if vivo is not None:
            partido = {**partido, "estado": vivo["estado"], "minuto": vivo["minuto"],
                       "goles_local": vivo["goles_local"], "goles_visitante": vivo["goles_visitante"]}
        resultado.append(partido)
    return resultado


def _league_rounds(season: int) -> list[str]:
    entry = _cached(
        f"liga-profesional-rounds:{season}",
        SEIS_HORAS,
        lambda: api_football.get_fixture_rounds(teams.LIGA_PROFESIONAL, season),
        [],
    )
    return entry.value


def _ultima_fecha_liga(league_id: int, season: int) -> list[dict]:
    desde, hasta = _rango_fechas(season)
    if league_id == teams.LIGA_PROFESIONAL:
        return api_football.get_latest_round_fixtures(league_id, season)
    return api_football.get_fixtures_by_date_range(
        league_id,
        season,
        desde,
        hasta,
    )[-5:]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/proximos-partidos")
def proximos_partidos(
    fecha: int = Query(0, ge=0),
    season: int = Query(SEASON_DEFAULT, ge=SEASON_MIN, le=SEASON_MAX),
):
    rounds = _league_rounds(season)
    if fecha >= len(rounds):
        raise HTTPException(status_code=404, detail="Fecha fuera de rango")

    round_name = rounds[fecha]
    entry = _cached(
        f"proximos-partidos:{season}:{fecha}",
        SEIS_HORAS,
        lambda: api_football.get_fixtures_by_round(teams.LIGA_PROFESIONAL, season, round_name),
        [],
    )
    return {
        "partidos": entry.value,
        "fecha_actual": {"indice": fecha, "nombre": round_name},
        "navegacion": {
            "anterior": fecha - 1 if fecha > 0 else None,
            "siguiente": fecha + 1 if fecha + 1 < len(rounds) else None,
            "total": len(rounds),
        },
        "actualizado_hace": entry.fetched_at,
        "stale": entry.is_stale,
    }


@app.get("/ultima-fecha")
def ultima_fecha(season: int = Query(SEASON_DEFAULT, ge=SEASON_MIN, le=SEASON_MAX)):
    entry = _cached(
        f"ultima-fecha:{season}",
        SEIS_HORAS,
        lambda: [f for liga in teams.COMPETICIONES for f in _ultima_fecha_liga(liga, season)],
        [],
    )
    return {"partidos": entry.value, "actualizado_hace": entry.fetched_at, "stale": entry.is_stale}


@app.get("/tabla")
def tabla(season: int = Query(SEASON_DEFAULT, ge=SEASON_MIN, le=SEASON_MAX)):
    entry = _cached(
        f"tabla:{season}",
        SEIS_HORAS,
        lambda: api_football.get_standings(teams.LIGA_PROFESIONAL, season),
        [],
    )
    return {"posiciones": entry.value, "actualizado_hace": entry.fetched_at, "stale": entry.is_stale}


@app.get("/equipos")
def equipos():
    return {"equipos": teams.list_teams()}


@app.get("/equipo/{nombre}")
def equipo(nombre: str):
    team = teams.get_team(nombre)
    if team is None:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")

    entry = _cached(
        f"equipo:{nombre}",
        UNA_HORA,
        lambda: {
            "estadisticas": api_football.get_team_statistics(team.id, teams.preferred_league_id(team), teams.SEASON),
            "resultados_recientes": api_football.get_recent_team_fixtures(
                team.id,
                teams.preferred_league_id(team),
                teams.SEASON,
                TEMPORADA_DESDE,
                TEMPORADA_HASTA,
                count=5,
            ),
        },
        None,
    )
    if entry.value is None:
        # Única excepción a "nunca 5xx": no hay ningún dato previo de este
        # equipo en memoria (primer request en frío) y la llamada falló.
        raise HTTPException(status_code=503, detail="Sin datos disponibles, intentá de nuevo en un momento")

    return {**entry.value, "actualizado_hace": entry.fetched_at, "stale": entry.is_stale}


@app.get("/partido/{fixture_id}/lineups")
def partido_lineups(fixture_id: int):
    entry = _cached(
        f"partido-lineups:{fixture_id}",
        SEIS_HORAS,
        lambda: api_football.get_lineups(fixture_id),
        {"local": None, "visitante": None},
    )
    return entry.value


@app.get("/partido/{fixture_id}")
def partido(fixture_id: int):
    entry = _cached(
        f"partido:{fixture_id}",
        UNA_HORA,
        lambda: api_football.get_fixture_detail(fixture_id),
        None,
    )
    if entry.value is None:
        raise HTTPException(status_code=503, detail="Sin datos disponibles, intentá de nuevo en un momento")

    detalle = dict(entry.value)
    vivo = next((p for p in _live_snapshot() if p["id"] == fixture_id), None)
    if vivo is not None:
        detalle["estado"] = vivo["estado"]
        detalle["minuto"] = vivo["minuto"]
        detalle["goles_local"] = vivo["goles_local"]
        detalle["goles_visitante"] = vivo["goles_visitante"]

    return {**detalle, "actualizado_hace": entry.fetched_at, "stale": entry.is_stale}
