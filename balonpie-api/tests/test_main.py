from fastapi.testclient import TestClient

import api_football
import main
from main import app

client = TestClient(app)


def test_health_check_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_equipos_lists_seeded_teams():
    response = client.get("/equipos")
    assert response.status_code == 200
    equipos = response.json()["equipos"]
    nombres = [equipo["nombre"] for equipo in equipos]
    assert "River Plate" in nombres
    assert "Boca Juniors" in nombres
    assert all("escudo" in equipo for equipo in equipos)
    assert all("competencia" in equipo for equipo in equipos)


def test_equipo_returns_404_for_unknown_slug():
    response = client.get("/equipo/equipo-inexistente")
    assert response.status_code == 404


def test_equipo_returns_statistics_and_recent_results(monkeypatch):
    calls = []

    monkeypatch.setattr(
        api_football,
        "get_team_statistics",
        lambda team_id, league_id, season, client=None: calls.append(("stats", team_id, league_id, season)) or {"equipo": "River Plate", "escudo": "https://media.api-sports.io/football/teams/435.png", "liga": "Liga Profesional Argentina", "partidos_jugados": 15, "ganados": 9, "empatados": 3, "perdidos": 3, "goles_a_favor": 28, "goles_en_contra": 14, "forma": ["W", "W", "D", "L", "W"]},
    )
    monkeypatch.setattr(
        api_football,
        "get_recent_team_fixtures",
        lambda team_id, league_id, season, from_date, to_date, count=5, client=None: calls.append(("fixtures", team_id, league_id, season, from_date, to_date, count)) or [],
    )
    main.cache = main.TTLCache()

    response = client.get("/equipo/river-plate")

    assert response.status_code == 200
    body = response.json()
    assert body["estadisticas"]["equipo"] == "River Plate"
    assert body["estadisticas"]["escudo"] == "https://media.api-sports.io/football/teams/435.png"
    assert body["resultados_recientes"] == []
    assert "actualizado_hace" in body
    assert body["stale"] is False
    assert calls == [("stats", 435, 128, 2024), ("fixtures", 435, 128, 2024, "2024-01-01", "2024-12-31", 5)]


def test_proximos_partidos_returns_requested_round_with_navigation(monkeypatch):
    monkeypatch.setattr(
        api_football,
        "get_fixture_rounds",
        lambda league_id, season, client=None: ["2nd Phase - 1", "2nd Phase - 2", "2nd Phase - 3"],
    )
    monkeypatch.setattr(
        api_football,
        "get_fixtures_by_round",
        lambda league_id, season, round_name, client=None: [{"id": 1002, "round": round_name}],
    )
    main.cache = main.TTLCache()

    response = client.get("/proximos-partidos?fecha=1")

    assert response.status_code == 200
    body = response.json()
    assert body["partidos"] == [{"id": 1002, "round": "2nd Phase - 2"}]
    assert body["fecha_actual"] == {"indice": 1, "nombre": "2nd Phase - 2"}
    assert body["navegacion"] == {"anterior": 0, "siguiente": 2, "total": 3}


def test_proximos_partidos_returns_404_when_round_index_is_out_of_range(monkeypatch):
    monkeypatch.setattr(
        api_football,
        "get_fixture_rounds",
        lambda league_id, season, client=None: ["2nd Phase - 1"],
    )
    main.cache = main.TTLCache()

    response = client.get("/proximos-partidos?fecha=5")

    assert response.status_code == 404


def test_ultima_fecha_aggregates_all_competitions(monkeypatch):
    monkeypatch.setattr(
        api_football,
        "get_latest_round_fixtures",
        lambda league_id, season, client=None: [{"id": league_id}] if league_id == 128 else [],
    )
    monkeypatch.setattr(
        api_football,
        "get_fixtures_by_date_range",
        lambda league_id, season, from_date, to_date, team_id=None, client=None: [{"id": league_id}] if league_id != 128 else [],
    )
    main.cache = main.TTLCache()

    response = client.get("/ultima-fecha")

    assert response.status_code == 200
    ids = [p["id"] for p in response.json()["partidos"]]
    assert sorted(ids) == sorted(main.teams.COMPETICIONES)


def test_tabla_returns_standings(monkeypatch):
    monkeypatch.setattr(api_football, "get_standings", lambda league_id, season, client=None: [{"posicion": 1, "equipo": "River Plate"}])
    main.cache = main.TTLCache()

    response = client.get("/tabla")

    assert response.status_code == 200
    assert response.json()["posiciones"] == [{"posicion": 1, "equipo": "River Plate"}]


def test_partido_overlays_live_snapshot_when_in_play(monkeypatch):
    monkeypatch.setattr(
        api_football,
        "get_fixture_detail",
        lambda fixture_id, client=None: {"id": fixture_id, "estado": "NS", "minuto": None, "goles_local": None, "goles_visitante": None, "eventos": [], "estadisticas": {}},
    )
    monkeypatch.setattr(
        api_football,
        "get_live_snapshot",
        lambda league_ids, client=None: [{"id": 1001, "estado": "1H", "minuto": 23, "goles_local": 1, "goles_visitante": 0}],
    )
    main.cache = main.TTLCache()

    response = client.get("/partido/1001")

    assert response.status_code == 200
    body = response.json()
    assert body["estado"] == "1H"
    assert body["minuto"] == 23
    assert body["goles_local"] == 1


def test_endpoint_serves_stale_data_when_refresh_fails(monkeypatch):
    fail = {"v": False}

    def get_standings(league_id, season, client=None):
        if fail["v"]:
            raise RuntimeError("API-Football no responde")
        return [{"posicion": 1, "equipo": "River Plate"}]

    monkeypatch.setattr(api_football, "get_standings", get_standings)
    main.cache = main.TTLCache()

    primera = client.get("/tabla")
    fail["v"] = True
    main.cache._store["tabla"] = (0.0, primera.json()["posiciones"])
    segunda = client.get("/tabla")

    assert segunda.status_code == 200
    assert segunda.json()["posiciones"] == [{"posicion": 1, "equipo": "River Plate"}]
    assert segunda.json()["stale"] is True


def test_equipo_returns_503_when_no_data_and_fetch_fails(monkeypatch):
    def falla(*args, **kwargs):
        raise RuntimeError("API-Football no responde")

    monkeypatch.setattr(api_football, "get_team_statistics", falla)
    monkeypatch.setattr(api_football, "get_recent_team_fixtures", falla)
    main.cache = main.TTLCache()

    response = client.get("/equipo/river-plate")

    assert response.status_code == 503


def test_proximos_partidos_caches_each_round_separately(monkeypatch):
    monkeypatch.setattr(
        api_football,
        "get_fixture_rounds",
        lambda league_id, season, client=None: ["2nd Phase - 1", "2nd Phase - 2"],
    )
    monkeypatch.setattr(
        api_football,
        "get_fixtures_by_round",
        lambda league_id, season, round_name, client=None: [{"id": 1000 if round_name.endswith("1") else 1001}],
    )
    main.cache = main.TTLCache()

    response1 = client.get("/proximos-partidos?fecha=0")
    assert response1.status_code == 200
    assert response1.json()["partidos"][0]["id"] == 1000

    response2 = client.get("/proximos-partidos?fecha=1")
    assert response2.status_code == 200
    assert response2.json()["partidos"][0]["id"] == 1001

    assert "proximos-partidos:0" in main.cache._store
    assert "proximos-partidos:1" in main.cache._store
