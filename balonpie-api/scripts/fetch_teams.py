import os
import sys
import unicodedata
from json import dumps as json_dumps
from pathlib import Path

import httpx
from dotenv import load_dotenv

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from teams import COMPETICIONES

load_dotenv()

BASE_URL = "https://v3.football.api-sports.io"
SEASON = 2024


def slugify(nombre: str) -> str:
    sin_acentos = unicodedata.normalize("NFKD", nombre).encode("ascii", "ignore").decode("ascii")
    return sin_acentos.lower().replace("'", "").replace(".", "").replace(" ", "-")


def format_team_line(*, team_id: int, nombre: str, liga_ids: tuple[int, ...], logo_url: str) -> str:
    escaped_nombre = json_dumps(nombre, ensure_ascii=True)
    escaped_logo_url = json_dumps(logo_url, ensure_ascii=True)
    return (
        f'    "{slugify(nombre)}": Team(id={team_id}, nombre={escaped_nombre}, '
        f"liga_ids={liga_ids}, logo_url={escaped_logo_url}),"
    )


def main():
    headers = {"x-apisports-key": os.environ["API_FOOTBALL_KEY"]}
    equipos = {}
    for liga_id in COMPETICIONES:
        response = httpx.get(
            f"{BASE_URL}/teams",
            headers=headers,
            params={"league": liga_id, "season": SEASON},
            timeout=10,
        )
        response.raise_for_status()
        for item in response.json()["response"]:
            team = item["team"]
            equipo = equipos.setdefault(
                team["id"],
                {"nombre": team["name"], "liga_ids": [], "logo_url": team["logo"]},
            )
            if liga_id not in equipo["liga_ids"]:
                equipo["liga_ids"].append(liga_id)

    for team_id, info in sorted(equipos.items()):
        liga_ids = tuple(info["liga_ids"])
        print(format_team_line(team_id=team_id, nombre=info["nombre"], liga_ids=liga_ids, logo_url=info["logo_url"]))


if __name__ == "__main__":
    main()
