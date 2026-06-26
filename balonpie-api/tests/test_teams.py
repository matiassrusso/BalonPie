from teams import LIGA_PROFESIONAL, SUDAMERICANA, Team, get_team, list_teams, preferred_league_id, slug_for_id


def test_get_team_returns_known_team():
    assert get_team("river-plate") == Team(
        id=435,
        nombre="River Plate",
        liga_ids=(128, 130, 13),
        logo_url="https://media.api-sports.io/football/teams/435.png",
    )


def test_get_team_returns_none_for_unknown_slug():
    assert get_team("equipo-inexistente") is None


def test_slug_for_id_returns_matching_slug():
    assert slug_for_id(451) == "boca-juniors"


def test_slug_for_id_returns_none_for_unknown_id():
    assert slug_for_id(999999) is None


def test_list_teams_is_sorted_by_name():
    nombres = [equipo["nombre"] for equipo in list_teams()]
    assert nombres == sorted(nombres)


def test_list_teams_includes_logo_url_as_escudo():
    equipos = list_teams()

    assert equipos[0]["escudo"].startswith("https://media.api-sports.io/football/teams/")


def test_list_teams_includes_preferred_competition_name():
    equipos = list_teams()

    river = next(equipo for equipo in equipos if equipo["slug"] == "river-plate")

    assert river["competencia"] == "Liga Profesional"


def test_preferred_league_id_prioritizes_liga_profesional():
    team = Team(id=1, nombre="Equipo", liga_ids=(130, LIGA_PROFESIONAL, 13), logo_url="https://example.com/logo.png")

    assert preferred_league_id(team) == LIGA_PROFESIONAL


def test_preferred_league_id_falls_back_to_first_competition():
    team = Team(id=1, nombre="Equipo", liga_ids=(13, 11), logo_url="https://example.com/logo.png")

    assert preferred_league_id(team) == 13


def test_sudamericana_uses_api_football_competition_id():
    assert SUDAMERICANA == 11
