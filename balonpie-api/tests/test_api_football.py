import os

import api_football
from teams import Team

# Set a dummy API key for tests so _headers() doesn't fail
os.environ.setdefault("API_FOOTBALL_KEY", "test-key")


FIXTURE_PROGRAMADO = {
    "fixture": {"id": 1001, "date": "2026-06-28T20:00:00+00:00", "status": {"short": "NS", "elapsed": None}},
    "league": {"id": 128, "name": "Liga Profesional Argentina"},
    "teams": {
        "home": {"id": 435, "name": "River Plate", "logo": "https://media.api-sports.io/football/teams/435.png"},
        "away": {"id": 451, "name": "Boca Juniors", "logo": "https://media.api-sports.io/football/teams/451.png"},
    },
    "goals": {"home": None, "away": None},
}


def test_transform_fixture_maps_basic_fields():
    resultado = api_football.transform_fixture(FIXTURE_PROGRAMADO)

    assert resultado == {
        "id": 1001,
        "fecha": "2026-06-28T20:00:00+00:00",
        "estado": "NS",
        "minuto": None,
        "competencia": "Liga Profesional Argentina",
        "equipo_local": "River Plate",
        "equipo_local_slug": "river-plate",
        "escudo_local": "https://media.api-sports.io/football/teams/435.png",
        "equipo_visitante": "Boca Juniors",
        "equipo_visitante_slug": "boca-juniors",
        "escudo_visitante": "https://media.api-sports.io/football/teams/451.png",
        "goles_local": None,
        "goles_visitante": None,
    }


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        pass

    def json(self):
        return self._payload


class FakeClient:
    def __init__(self, payload):
        self._payload = payload
        self.calls = []

    def get(self, url, headers, params, timeout):
        self.calls.append({"url": url, "params": params})
        return FakeResponse(self._payload)


def test_get_next_fixtures_calls_fixtures_endpoint_with_next_param():
    fake = FakeClient({"response": [FIXTURE_PROGRAMADO]})

    resultado = api_football.get_next_fixtures(128, 2025, count=5, client=fake)

    assert resultado == [api_football.transform_fixture(FIXTURE_PROGRAMADO)]
    assert fake.calls[0]["url"] == "https://v3.football.api-sports.io/fixtures"
    assert fake.calls[0]["params"] == {"league": 128, "season": 2025, "next": 5}


def test_get_fixture_rounds_calls_rounds_endpoint():
    fake = FakeClient({"response": ["2nd Phase - 26", "2nd Phase - 27"]})

    resultado = api_football.get_fixture_rounds(128, 2025, client=fake)

    assert resultado == ["2nd Phase - 26", "2nd Phase - 27"]
    assert fake.calls[0]["url"] == "https://v3.football.api-sports.io/fixtures/rounds"
    assert fake.calls[0]["params"] == {"league": 128, "season": 2025}


def test_get_fixtures_by_round_calls_fixtures_endpoint_with_round_param():
    fake = FakeClient({"response": [FIXTURE_PROGRAMADO]})

    resultado = api_football.get_fixtures_by_round(128, 2025, "2nd Phase - 27", client=fake)

    assert resultado == [api_football.transform_fixture(FIXTURE_PROGRAMADO)]
    assert fake.calls[0]["params"] == {"league": 128, "season": 2025, "round": "2nd Phase - 27"}


def test_get_fixtures_by_date_range_calls_fixtures_endpoint_with_from_to_params():
    fake = FakeClient({"response": [FIXTURE_PROGRAMADO]})

    resultado = api_football.get_fixtures_by_date_range(130, 2024, "2024-01-01", "2024-12-31", client=fake)

    assert resultado == [api_football.transform_fixture(FIXTURE_PROGRAMADO)]
    assert fake.calls[0]["params"] == {"league": 130, "season": 2024, "from": "2024-01-01", "to": "2024-12-31"}


def test_get_latest_round_fixtures_uses_last_round_name():
    fake = FakeMultiEndpointClient(
        {
            "https://v3.football.api-sports.io/fixtures/rounds": {"response": ["2nd Phase - 26", "2nd Phase - 27"]},
            "https://v3.football.api-sports.io/fixtures": {"response": [FIXTURE_PROGRAMADO]},
        }
    )

    resultado = api_football.get_latest_round_fixtures(128, 2024, client=fake)

    assert resultado == [api_football.transform_fixture(FIXTURE_PROGRAMADO)]
    assert fake.calls[0]["params"] == {"league": 128, "season": 2024}
    assert fake.calls[1]["params"] == {"league": 128, "season": 2024, "round": "2nd Phase - 27"}


def test_get_live_snapshot_filters_by_competition_ids():
    partido_liga = {**FIXTURE_PROGRAMADO, "league": {"id": 128, "name": "Liga Profesional Argentina"}}
    partido_otra_liga = {**FIXTURE_PROGRAMADO, "league": {"id": 999, "name": "Otra liga"}}
    fake = FakeClient({"response": [partido_liga, partido_otra_liga]})

    resultado = api_football.get_live_snapshot([128, 130, 13, 14], client=fake)

    assert len(resultado) == 1
    assert resultado[0]["competencia"] == "Liga Profesional Argentina"
    assert fake.calls[0]["params"] == {"live": "all"}


POSICION_RAW = {
    "rank": 1,
    "team": {"id": 435, "name": "River Plate", "logo": "https://media.api-sports.io/football/teams/435.png"},
    "points": 30,
    "goalsDiff": 12,
    "all": {"played": 15, "win": 9, "draw": 3, "lose": 3},
    "form": "WWDLW",
}


def test_transform_standing_maps_fields():
    resultado = api_football.transform_standing(POSICION_RAW)

    assert resultado == {
        "posicion": 1,
        "equipo": "River Plate",
        "slug": "river-plate",
        "escudo": "https://media.api-sports.io/football/teams/435.png",
        "puntos": 30,
        "jugados": 15,
        "ganados": 9,
        "empatados": 3,
        "perdidos": 3,
        "diferencia_goles": 12,
        "forma": ["W", "W", "D", "L", "W"],
    }


def test_get_standings_unwraps_nested_response_shape():
    fake = FakeClient({"response": [{"league": {"standings": [[POSICION_RAW]]}}]})

    resultado = api_football.get_standings(128, 2025, client=fake)

    assert resultado == [api_football.transform_standing(POSICION_RAW)]
    assert fake.calls[0]["params"] == {"league": 128, "season": 2025}


ESTADISTICAS_RAW = {
    "team": {"id": 435, "name": "River Plate", "logo": "https://media.api-sports.io/football/teams/435.png"},
    "league": {"name": "Liga Profesional Argentina"},
    "fixtures": {
        "played": {"total": 15},
        "wins": {"total": 9},
        "draws": {"total": 3},
        "loses": {"total": 3},
    },
    "goals": {
        "for": {"total": {"total": 28}},
        "against": {"total": {"total": 14}},
    },
    "form": "WWDLW",
}


def test_transform_team_statistics_maps_fields():
    resultado = api_football.transform_team_statistics(ESTADISTICAS_RAW)

    assert resultado == {
        "equipo": "River Plate",
        "escudo": "https://media.api-sports.io/football/teams/435.png",
        "liga": "Liga Profesional Argentina",
        "partidos_jugados": 15,
        "ganados": 9,
        "empatados": 3,
        "perdidos": 3,
        "goles_a_favor": 28,
        "goles_en_contra": 14,
        "forma": ["W", "W", "D", "L", "W"],
    }


def test_get_team_statistics_calls_statistics_endpoint():
    fake = FakeClient({"response": ESTADISTICAS_RAW})

    resultado = api_football.get_team_statistics(435, 128, 2025, client=fake)

    assert resultado == api_football.transform_team_statistics(ESTADISTICAS_RAW)
    assert fake.calls[0]["url"] == "https://v3.football.api-sports.io/teams/statistics"
    assert fake.calls[0]["params"] == {"team": 435, "league": 128, "season": 2025}


def test_get_recent_team_fixtures_calls_fixtures_endpoint_with_team_and_date_params():
    fake = FakeClient({"response": [FIXTURE_PROGRAMADO]})

    resultado = api_football.get_recent_team_fixtures(
        435,
        128,
        2025,
        "2024-01-01",
        "2024-12-31",
        count=5,
        client=fake,
    )

    assert resultado == [api_football.transform_fixture(FIXTURE_PROGRAMADO)]
    assert fake.calls[0]["params"] == {
        "team": 435,
        "league": 128,
        "season": 2025,
        "from": "2024-01-01",
        "to": "2024-12-31",
    }


def test_get_recent_team_fixtures_returns_only_requested_count_from_end():
    fixtures = [{"response": [FIXTURE_PROGRAMADO, {**FIXTURE_PROGRAMADO, "fixture": {**FIXTURE_PROGRAMADO["fixture"], "id": 1002}}, {**FIXTURE_PROGRAMADO, "fixture": {**FIXTURE_PROGRAMADO["fixture"], "id": 1003}}]}]
    fake = FakeClient(fixtures[0])

    resultado = api_football.get_recent_team_fixtures(
        435,
        128,
        2025,
        "2024-01-01",
        "2024-12-31",
        count=2,
        client=fake,
    )

    assert [fixture["id"] for fixture in resultado] == [1002, 1003]


EVENTOS_RAW = [
    {"time": {"elapsed": 23}, "type": "Goal", "detail": "Normal Goal", "team": {"name": "River Plate"}, "player": {"name": "J. Álvarez"}},
    {"time": {"elapsed": 41}, "type": "Card", "detail": "Yellow Card", "team": {"name": "Boca Juniors"}, "player": {"name": "M. Rojo"}},
    {"time": {"elapsed": 60}, "type": "subst", "detail": "Substitution 1", "team": {"name": "River Plate"}, "player": {"name": "X"}},
]

ESTADISTICAS_PARTIDO_RAW = [
    {"team": {"name": "River Plate"}, "statistics": [{"type": "Ball Possession", "value": "58%"}, {"type": "Total Shots", "value": 14}]},
    {"team": {"name": "Boca Juniors"}, "statistics": [{"type": "Ball Possession", "value": "42%"}, {"type": "Total Shots", "value": 9}]},
]


def test_transform_fixture_events_keeps_only_goals_and_cards():
    resultado = api_football.transform_fixture_events(EVENTOS_RAW)

    assert resultado == [
        {"minuto": 23, "tipo": "Goal", "detalle": "Normal Goal", "equipo": "River Plate", "jugador": "J. Álvarez"},
        {"minuto": 41, "tipo": "Card", "detalle": "Yellow Card", "equipo": "Boca Juniors", "jugador": "M. Rojo"},
    ]


def test_transform_fixture_statistics_keys_by_team_name():
    resultado = api_football.transform_fixture_statistics(ESTADISTICAS_PARTIDO_RAW)

    assert resultado == {
        "River Plate": {"Ball Possession": "58%", "Total Shots": 14},
        "Boca Juniors": {"Ball Possession": "42%", "Total Shots": 9},
    }


def test_transform_fixture_detail_combines_fixture_events_and_statistics():
    resultado = api_football.transform_fixture_detail(FIXTURE_PROGRAMADO, EVENTOS_RAW, ESTADISTICAS_PARTIDO_RAW)

    assert resultado["id"] == 1001
    assert resultado["eventos"] == api_football.transform_fixture_events(EVENTOS_RAW)
    assert resultado["estadisticas"] == api_football.transform_fixture_statistics(ESTADISTICAS_PARTIDO_RAW)


class FakeMultiEndpointClient:
    def __init__(self, payloads: dict):
        self._payloads = payloads
        self.calls = []

    def get(self, url, headers, params, timeout):
        self.calls.append({"url": url, "params": params})
        return FakeResponse(self._payloads[url])


def test_get_fixture_detail_combines_three_endpoints():
    fake = FakeMultiEndpointClient(
        {
            "https://v3.football.api-sports.io/fixtures": {"response": [FIXTURE_PROGRAMADO]},
            "https://v3.football.api-sports.io/fixtures/events": {"response": EVENTOS_RAW},
            "https://v3.football.api-sports.io/fixtures/statistics": {"response": ESTADISTICAS_PARTIDO_RAW},
        }
    )

    resultado = api_football.get_fixture_detail(1001, client=fake)

    assert resultado["id"] == 1001
    assert resultado["eventos"] == api_football.transform_fixture_events(EVENTOS_RAW)
    assert resultado["estadisticas"] == api_football.transform_fixture_statistics(ESTADISTICAS_PARTIDO_RAW)
    assert fake.calls[0]["params"] == {"id": 1001}
    assert fake.calls[1]["params"] == {"fixture": 1001}
    assert fake.calls[2]["params"] == {"fixture": 1001}
