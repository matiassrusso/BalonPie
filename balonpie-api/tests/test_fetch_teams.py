from scripts.fetch_teams import COMPETICIONES, format_team_line, slugify
from teams import SUDAMERICANA


def test_slugify_removes_accents_and_punctuation():
    assert slugify("Argentino Monte Maíz") == "argentino-monte-maiz"


def test_competiciones_uses_correct_sudamericana_id():
    assert SUDAMERICANA in COMPETICIONES
    assert 14 not in COMPETICIONES


def test_format_team_line_escapes_non_ascii_names():
    line = format_team_line(
        team_id=18764,
        nombre="Argentino Monte Maíz",
        liga_ids=(130,),
        logo_url="https://media.api-sports.io/football/teams/18764.png",
    )

    assert "\\u00ed" in line
    assert "Argentino Monte Ma" in line
