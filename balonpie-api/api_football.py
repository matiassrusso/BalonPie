import os

import httpx

import teams

BASE_URL = "https://v3.football.api-sports.io"


def _headers() -> dict:
    return {"x-apisports-key": os.environ["API_FOOTBALL_KEY"]}


def _get(path: str, params: dict, client=None) -> list | dict:
    client = client or httpx
    response = client.get(f"{BASE_URL}{path}", headers=_headers(), params=params, timeout=10)
    response.raise_for_status()
    return response.json()["response"]


def transform_fixture(raw: dict) -> dict:
    fixture = raw["fixture"]
    league = raw["league"]
    equipos = raw["teams"]
    goles = raw["goals"]
    return {
        "id": fixture["id"],
        "fecha": fixture["date"],
        "estado": fixture["status"]["short"],
        "minuto": fixture["status"]["elapsed"],
        "competencia": league["name"],
        "equipo_local": equipos["home"]["name"],
        "equipo_local_slug": teams.slug_for_id(equipos["home"]["id"]),
        "escudo_local": equipos["home"]["logo"],
        "equipo_visitante": equipos["away"]["name"],
        "equipo_visitante_slug": teams.slug_for_id(equipos["away"]["id"]),
        "escudo_visitante": equipos["away"]["logo"],
        "goles_local": goles["home"],
        "goles_visitante": goles["away"],
    }


def get_next_fixtures(league_id: int, season: int, count: int = 5, client=None) -> list[dict]:
    raw = _get("/fixtures", {"league": league_id, "season": season, "next": count}, client)
    return [transform_fixture(f) for f in raw]


def get_fixture_rounds(league_id: int, season: int, client=None) -> list[str]:
    raw = _get("/fixtures/rounds", {"league": league_id, "season": season}, client)
    return [str(round_name) for round_name in raw]


def get_fixtures_by_round(league_id: int, season: int, round_name: str, client=None) -> list[dict]:
    raw = _get("/fixtures", {"league": league_id, "season": season, "round": round_name}, client)
    return [transform_fixture(f) for f in raw]


def get_fixtures_by_date_range(
    league_id: int,
    season: int,
    from_date: str,
    to_date: str,
    team_id: int | None = None,
    client=None,
) -> list[dict]:
    params = {"league": league_id, "season": season, "from": from_date, "to": to_date}
    if team_id is not None:
        params["team"] = team_id
    raw = _get("/fixtures", params, client)
    return [transform_fixture(f) for f in raw]


def get_latest_round_fixtures(league_id: int, season: int, client=None) -> list[dict]:
    rounds = get_fixture_rounds(league_id, season, client=client)
    return get_fixtures_by_round(league_id, season, rounds[-1], client=client)


def get_live_snapshot(league_ids: list[int], client=None) -> list[dict]:
    raw = _get("/fixtures", {"live": "all"}, client)
    return [transform_fixture(f) for f in raw if f["league"]["id"] in league_ids]


def transform_standing(raw: dict) -> dict:
    equipo = raw["team"]
    return {
        "posicion": raw["rank"],
        "equipo": equipo["name"],
        "slug": teams.slug_for_id(equipo["id"]),
        "escudo": equipo["logo"],
        "puntos": raw["points"],
        "jugados": raw["all"]["played"],
        "ganados": raw["all"]["win"],
        "empatados": raw["all"]["draw"],
        "perdidos": raw["all"]["lose"],
        "diferencia_goles": raw["goalsDiff"],
        "forma": list(raw["form"]) if raw.get("form") else [],
    }


def get_standings(league_id: int, season: int, client=None) -> list[dict]:
    raw = _get("/standings", {"league": league_id, "season": season}, client)
    posiciones = raw[0]["league"]["standings"][0]
    return [transform_standing(p) for p in posiciones]


def transform_team_statistics(raw: dict) -> dict:
    fixtures = raw["fixtures"]
    goles = raw["goals"]
    return {
        "equipo": raw["team"]["name"],
        "escudo": raw["team"]["logo"],
        "liga": raw["league"]["name"],
        "partidos_jugados": fixtures["played"]["total"],
        "ganados": fixtures["wins"]["total"],
        "empatados": fixtures["draws"]["total"],
        "perdidos": fixtures["loses"]["total"],
        "goles_a_favor": goles["for"]["total"]["total"],
        "goles_en_contra": goles["against"]["total"]["total"],
        "forma": list(raw["form"]) if raw.get("form") else [],
    }


def get_team_statistics(team_id: int, league_id: int, season: int, client=None) -> dict:
    raw = _get("/teams/statistics", {"team": team_id, "league": league_id, "season": season}, client)
    return transform_team_statistics(raw)


def get_recent_team_fixtures(
    team_id: int,
    league_id: int,
    season: int,
    from_date: str,
    to_date: str,
    count: int = 5,
    client=None,
) -> list[dict]:
    fixtures = get_fixtures_by_date_range(
        league_id,
        season,
        from_date,
        to_date,
        team_id=team_id,
        client=client,
    )
    return fixtures[-count:]


def transform_fixture_events(raw_events: list[dict]) -> list[dict]:
    eventos = []
    for evento in raw_events:
        if evento["type"] not in ("Goal", "Card"):
            continue
        eventos.append(
            {
                "minuto": evento["time"]["elapsed"],
                "tipo": evento["type"],
                "detalle": evento["detail"],
                "equipo": evento["team"]["name"],
                "jugador": evento["player"]["name"],
            }
        )
    return eventos


def transform_fixture_statistics(raw_stats: list[dict]) -> dict:
    return {
        equipo_stats["team"]["name"]: {stat["type"]: stat["value"] for stat in equipo_stats["statistics"]}
        for equipo_stats in raw_stats
    }


def transform_fixture_detail(fixture_raw: dict, events_raw: list[dict], stats_raw: list[dict]) -> dict:
    detalle = transform_fixture(fixture_raw)
    detalle["eventos"] = transform_fixture_events(events_raw)
    detalle["estadisticas"] = transform_fixture_statistics(stats_raw)
    return detalle


def transform_lineup_player(raw: dict) -> dict:
    player = raw["player"]
    return {
        "nombre": player["name"],
        "pos": player.get("pos", ""),
        "grid": player.get("grid"),
    }


def get_lineups(fixture_id: int, client=None) -> dict:
    raw = _get("/fixtures/lineups", {"fixture": fixture_id}, client)
    if not raw or len(raw) < 2:
        return {"local": None, "visitante": None}

    def transform_team(data: dict) -> dict:
        coach = data.get("coach") or {}
        return {
            "equipo": data["team"]["name"],
            "formacion": data.get("formation", ""),
            "once": [transform_lineup_player(p) for p in data.get("startXI", [])],
            "suplentes": [p["player"]["name"] for p in data.get("substitutes", [])],
            "dt": coach.get("name"),
        }

    return {"local": transform_team(raw[0]), "visitante": transform_team(raw[1])}


def get_fixture_detail(fixture_id: int, client=None) -> dict:
    fixture_raw = _get("/fixtures", {"id": fixture_id}, client)[0]
    events_raw = _get("/fixtures/events", {"fixture": fixture_id}, client)
    stats_raw = _get("/fixtures/statistics", {"fixture": fixture_id}, client)
    return transform_fixture_detail(fixture_raw, events_raw, stats_raw)
