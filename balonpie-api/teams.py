from dataclasses import dataclass

SEASON = 2024
LIGA_PROFESIONAL = 128
COPA_ARGENTINA = 130
LIBERTADORES = 13
SUDAMERICANA = 11
COMPETICIONES = [LIGA_PROFESIONAL, COPA_ARGENTINA, LIBERTADORES, SUDAMERICANA]
COMPETICION_NOMBRES = {
    LIGA_PROFESIONAL: "Liga Profesional",
    COPA_ARGENTINA: "Copa Argentina",
    LIBERTADORES: "Copa Libertadores",
    SUDAMERICANA: "Copa Sudamericana",
}


@dataclass(frozen=True)
class Team:
    id: int
    nombre: str
    liga_ids: tuple[int, ...]
    logo_url: str


# Seed generado desde `python scripts/fetch_teams.py` usando las 4
# competiciones configuradas para la temporada 2024.
TEAMS: dict[str, Team] = {
    "internacional": Team(id=119, nombre="Internacional", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/119.png"),
    "botafogo": Team(id=120, nombre="Botafogo", liga_ids=(13,), logo_url="https://media.api-sports.io/football/teams/120.png"),
    "palmeiras": Team(id=121, nombre="Palmeiras", liga_ids=(13,), logo_url="https://media.api-sports.io/football/teams/121.png"),
    "fluminense": Team(id=124, nombre="Fluminense", liga_ids=(13,), logo_url="https://media.api-sports.io/football/teams/124.png"),
    "sao-paulo": Team(id=126, nombre="Sao Paulo", liga_ids=(13,), logo_url="https://media.api-sports.io/football/teams/126.png"),
    "flamengo": Team(id=127, nombre="Flamengo", liga_ids=(13,), logo_url="https://media.api-sports.io/football/teams/127.png"),
    "gremio": Team(id=130, nombre="Gremio", liga_ids=(13,), logo_url="https://media.api-sports.io/football/teams/130.png"),
    "corinthians": Team(id=131, nombre="Corinthians", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/131.png"),
    "atletico-paranaense": Team(id=134, nombre="Atletico Paranaense", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/134.png"),
    "cruzeiro": Team(id=135, nombre="Cruzeiro", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/135.png"),
    "fortaleza-ec": Team(id=154, nombre="Fortaleza EC", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/154.png"),
    "gimnasia-lp": Team(id=434, nombre="Gimnasia L.P.", liga_ids=(128, 130), logo_url="https://media.api-sports.io/football/teams/434.png"),
    "river-plate": Team(id=435, nombre="River Plate", liga_ids=(128, 130, 13), logo_url="https://media.api-sports.io/football/teams/435.png"),
    "racing-club": Team(id=436, nombre="Racing Club", liga_ids=(128, 130, 11), logo_url="https://media.api-sports.io/football/teams/436.png"),
    "rosario-central": Team(id=437, nombre="Rosario Central", liga_ids=(128, 130, 13, 11), logo_url="https://media.api-sports.io/football/teams/437.png"),
    "velez-sarsfield": Team(id=438, nombre="Velez Sarsfield", liga_ids=(128, 130), logo_url="https://media.api-sports.io/football/teams/438.png"),
    "godoy-cruz": Team(id=439, nombre="Godoy Cruz", liga_ids=(128, 130, 13), logo_url="https://media.api-sports.io/football/teams/439.png"),
    "belgrano-cordoba": Team(id=440, nombre="Belgrano Cordoba", liga_ids=(128, 130, 11), logo_url="https://media.api-sports.io/football/teams/440.png"),
    "union-santa-fe": Team(id=441, nombre="Union Santa Fe", liga_ids=(128, 130), logo_url="https://media.api-sports.io/football/teams/441.png"),
    "defensa-y-justicia": Team(id=442, nombre="Defensa Y Justicia", liga_ids=(128, 130, 11), logo_url="https://media.api-sports.io/football/teams/442.png"),
    "olimpo-bahia-blanca": Team(id=443, nombre="Olimpo Bahia Blanca", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/443.png"),
    "huracan": Team(id=445, nombre="Huracan", liga_ids=(128, 130), logo_url="https://media.api-sports.io/football/teams/445.png"),
    "lanus": Team(id=446, nombre="Lanus", liga_ids=(128, 130, 11), logo_url="https://media.api-sports.io/football/teams/446.png"),
    "chacarita-juniors": Team(id=447, nombre="Chacarita Juniors", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/447.png"),
    "colon-santa-fe": Team(id=448, nombre="Colon Santa Fe", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/448.png"),
    "banfield": Team(id=449, nombre="Banfield", liga_ids=(128, 130), logo_url="https://media.api-sports.io/football/teams/449.png"),
    "estudiantes-lp": Team(id=450, nombre="Estudiantes L.P.", liga_ids=(128, 130, 13), logo_url="https://media.api-sports.io/football/teams/450.png"),
    "boca-juniors": Team(id=451, nombre="Boca Juniors", liga_ids=(128, 130, 11), logo_url="https://media.api-sports.io/football/teams/451.png"),
    "tigre": Team(id=452, nombre="Tigre", liga_ids=(128, 130), logo_url="https://media.api-sports.io/football/teams/452.png"),
    "independiente": Team(id=453, nombre="Independiente", liga_ids=(128, 130), logo_url="https://media.api-sports.io/football/teams/453.png"),
    "temperley": Team(id=454, nombre="Temperley", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/454.png"),
    "atletico-tucuman": Team(id=455, nombre="Atletico Tucuman", liga_ids=(128, 130), logo_url="https://media.api-sports.io/football/teams/455.png"),
    "talleres-cordoba": Team(id=456, nombre="Talleres Cordoba", liga_ids=(128, 130, 13), logo_url="https://media.api-sports.io/football/teams/456.png"),
    "newells-old-boys": Team(id=457, nombre="Newells Old Boys", liga_ids=(128, 130), logo_url="https://media.api-sports.io/football/teams/457.png"),
    "argentinos-jrs": Team(id=458, nombre="Argentinos JRS", liga_ids=(128, 130, 11), logo_url="https://media.api-sports.io/football/teams/458.png"),
    "arsenal-sarandi": Team(id=459, nombre="Arsenal Sarandi", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/459.png"),
    "san-lorenzo": Team(id=460, nombre="San Lorenzo", liga_ids=(128, 130, 13), logo_url="https://media.api-sports.io/football/teams/460.png"),
    "san-martin-sj": Team(id=461, nombre="San Martin S.J.", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/461.png"),
    "agropecuario": Team(id=462, nombre="Agropecuario", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/462.png"),
    "atletico-de-rafaela": Team(id=465, nombre="Atletico DE Rafaela", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/465.png"),
    "atletico-mitre": Team(id=466, nombre="Atletico Mitre", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/466.png"),
    "independ-rivadavia": Team(id=473, nombre="Independ. Rivadavia", liga_ids=(128, 130), logo_url="https://media.api-sports.io/football/teams/473.png"),
    "sarmiento-junin": Team(id=474, nombre="Sarmiento Junin", liga_ids=(128, 130), logo_url="https://media.api-sports.io/football/teams/474.png"),
    "deportivo-riestra": Team(id=476, nombre="Deportivo Riestra", liga_ids=(128, 130), logo_url="https://media.api-sports.io/football/teams/476.png"),
    "instituto-cordoba": Team(id=478, nombre="Instituto Cordoba", liga_ids=(128, 130), logo_url="https://media.api-sports.io/football/teams/478.png"),
    "quilmes": Team(id=480, nombre="Quilmes", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/480.png"),
    "los-andes": Team(id=483, nombre="Los Andes", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/483.png"),
    "san-martin-tucuman": Team(id=485, nombre="San Martin Tucuman", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/485.png"),
    "douglas-haig": Team(id=789, nombre="Douglas Haig", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/789.png"),
    "rb-bragantino": Team(id=794, nombre="RB Bragantino", liga_ids=(13, 11), logo_url="https://media.api-sports.io/football/teams/794.png"),
    "atletico-mg": Team(id=1062, nombre="Atletico-MG", liga_ids=(13,), logo_url="https://media.api-sports.io/football/teams/1062.png"),
    "platense": Team(id=1064, nombre="Platense", liga_ids=(128, 130), logo_url="https://media.api-sports.io/football/teams/1064.png"),
    "central-cordoba-de-santiago": Team(id=1065, nombre="Central Cordoba de Santiago", liga_ids=(128, 130), logo_url="https://media.api-sports.io/football/teams/1065.png"),
    "gimnasia-m": Team(id=1066, nombre="Gimnasia M.", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/1066.png"),
    "defensores-de-belgrano": Team(id=1067, nombre="Defensores De Belgrano", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/1067.png"),
    "millonarios": Team(id=1125, nombre="Millonarios", liga_ids=(13,), logo_url="https://media.api-sports.io/football/teams/1125.png"),
    "independiente-medellin": Team(id=1128, nombre="Independiente Medellin", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/1128.png"),
    "junior": Team(id=1135, nombre="Junior", liga_ids=(13,), logo_url="https://media.api-sports.io/football/teams/1135.png"),
    "atletico-nacional": Team(id=1137, nombre="Atletico Nacional", liga_ids=(13,), logo_url="https://media.api-sports.io/football/teams/1137.png"),
    "america-de-cali": Team(id=1138, nombre="America de Cali", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/1138.png"),
    "alianza-valledupar": Team(id=1141, nombre="Alianza Valledupar", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/1141.png"),
    "deportes-tolima": Team(id=1142, nombre="Deportes Tolima", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/1142.png"),
    "aguilas-doradas": Team(id=1144, nombre="\u00c1guilas Doradas", liga_ids=(13,), logo_url="https://media.api-sports.io/football/teams/1144.png"),
    "delfin-sc": Team(id=1149, nombre="Delfin SC", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/1149.png"),
    "el-nacional": Team(id=1150, nombre="El Nacional", liga_ids=(13,), logo_url="https://media.api-sports.io/football/teams/1150.png"),
    "tecnico-universitario": Team(id=1151, nombre="Tecnico Universitario", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/1151.png"),
    "barcelona-sc": Team(id=1152, nombre="Barcelona SC", liga_ids=(13, 11), logo_url="https://media.api-sports.io/football/teams/1152.png"),
    "independiente-del-valle": Team(id=1153, nombre="Independiente del Valle", liga_ids=(13, 11), logo_url="https://media.api-sports.io/football/teams/1153.png"),
    "deportivo-cuenca": Team(id=1154, nombre="Deportivo Cuenca", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/1154.png"),
    "aucas": Team(id=1156, nombre="Aucas", liga_ids=(13,), logo_url="https://media.api-sports.io/football/teams/1156.png"),
    "universidad-catolica": Team(id=1157, nombre="Universidad Catolica", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/1157.png"),
    "ldu-de-quito": Team(id=1158, nombre="LDU de Quito", liga_ids=(13, 11), logo_url="https://media.api-sports.io/football/teams/1158.png"),
    "club-guarani": Team(id=1174, nombre="Club Guarani", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/1174.png"),
    "nacional-asuncion": Team(id=1175, nombre="Nacional Asuncion", liga_ids=(13, 11), logo_url="https://media.api-sports.io/football/teams/1175.png"),
    "cerro-porteno": Team(id=1176, nombre="Cerro Porteno", liga_ids=(13, 11), logo_url="https://media.api-sports.io/football/teams/1176.png"),
    "libertad-asuncion": Team(id=1179, nombre="Libertad Asuncion", liga_ids=(13, 11), logo_url="https://media.api-sports.io/football/teams/1179.png"),
    "olimpia": Team(id=1182, nombre="Olimpia", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/1182.png"),
    "sportivo-luqueno": Team(id=1183, nombre="Sportivo Luqueno", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/1183.png"),
    "sportivo-trinidense": Team(id=1187, nombre="Sportivo Trinidense", liga_ids=(13, 11), logo_url="https://media.api-sports.io/football/teams/1187.png"),
    "cuiaba": Team(id=1193, nombre="Cuiaba", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/1193.png"),
    "deportivo-laferrere": Team(id=1924, nombre="Deportivo Laferrere", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/1924.png"),
    "talleres-remedios": Team(id=1927, nombre="Talleres Remedios", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/1927.png"),
    "gimnasia-y-tiro": Team(id=1928, nombre="Gimnasia Y Tiro", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/1928.png"),
    "villa-mitre": Team(id=1938, nombre="Villa Mitre", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/1938.png"),
    "sportivo-las-parejas": Team(id=1950, nombre="Sportivo Las Parejas", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/1950.png"),
    "central-norte": Team(id=1951, nombre="Central Norte", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/1951.png"),
    "deportivo-maipu": Team(id=1954, nombre="Deportivo Maipu", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/1954.png"),
    "independiente-de-chivilcoy": Team(id=1960, nombre="Independiente De Chivilcoy", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/1960.png"),
    "midland": Team(id=1963, nombre="Midland", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/1963.png"),
    "colo-colo": Team(id=2315, nombre="Colo Colo", liga_ids=(13,), logo_url="https://media.api-sports.io/football/teams/2315.png"),
    "palestino": Team(id=2318, nombre="Palestino", liga_ids=(13, 11), logo_url="https://media.api-sports.io/football/teams/2318.png"),
    "everton-de-vina": Team(id=2325, nombre="Everton de Vina", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/2325.png"),
    "union-la-calera": Team(id=2326, nombre="Union La Calera", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/2326.png"),
    "huachipato": Team(id=2328, nombre="Huachipato", liga_ids=(13, 11), logo_url="https://media.api-sports.io/football/teams/2328.png"),
    "coquimbo-unido": Team(id=2330, nombre="Coquimbo Unido", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/2330.png"),
    "cobresal": Team(id=2331, nombre="Cobresal", liga_ids=(13,), logo_url="https://media.api-sports.io/football/teams/2331.png"),
    "penarol": Team(id=2348, nombre="Penarol", liga_ids=(13,), logo_url="https://media.api-sports.io/football/teams/2348.png"),
    "defensor-sporting": Team(id=2350, nombre="Defensor Sporting", liga_ids=(13,), logo_url="https://media.api-sports.io/football/teams/2350.png"),
    "danubio": Team(id=2352, nombre="Danubio", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/2352.png"),
    "club-nacional": Team(id=2356, nombre="Club Nacional", liga_ids=(13,), logo_url="https://media.api-sports.io/football/teams/2356.png"),
    "liverpool-montevideo": Team(id=2358, nombre="Liverpool Montevideo", liga_ids=(13,), logo_url="https://media.api-sports.io/football/teams/2358.png"),
    "racing-montevideo": Team(id=2359, nombre="Racing Montevideo", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/2359.png"),
    "wanderers": Team(id=2360, nombre="Wanderers", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/2360.png"),
    "cerro-largo": Team(id=2369, nombre="Cerro Largo", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/2369.png"),
    "estudiantes-de-rio-cuarto": Team(id=2424, nombre="Estudiantes de Rio Cuarto", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/2424.png"),
    "barracas-central": Team(id=2432, nombre="Barracas Central", liga_ids=(128, 130), logo_url="https://media.api-sports.io/football/teams/2432.png"),
    "universitario": Team(id=2540, nombre="Universitario", liga_ids=(13,), logo_url="https://media.api-sports.io/football/teams/2540.png"),
    "cesar-vallejo": Team(id=2541, nombre="Cesar Vallejo", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/2541.png"),
    "sporting-cristal": Team(id=2546, nombre="Sporting Cristal", liga_ids=(13,), logo_url="https://media.api-sports.io/football/teams/2546.png"),
    "alianza-lima": Team(id=2553, nombre="Alianza Lima", liga_ids=(13,), logo_url="https://media.api-sports.io/football/teams/2553.png"),
    "fbc-melgar": Team(id=2554, nombre="FBC Melgar", liga_ids=(13,), logo_url="https://media.api-sports.io/football/teams/2554.png"),
    "sport-huancayo": Team(id=2555, nombre="Sport Huancayo", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/2555.png"),
    "deportivo-tachira-fc": Team(id=2807, nombre="Deportivo Tachira FC", liga_ids=(13,), logo_url="https://media.api-sports.io/football/teams/2807.png"),
    "caracas-fc": Team(id=2808, nombre="Caracas FC", liga_ids=(13,), logo_url="https://media.api-sports.io/football/teams/2808.png"),
    "carabobo-fc": Team(id=2810, nombre="Carabobo FC", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/2810.png"),
    "deportivo-la-guaira": Team(id=2813, nombre="Deportivo La Guaira", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/2813.png"),
    "portuguesa-fc": Team(id=2814, nombre="Portuguesa FC", liga_ids=(13,), logo_url="https://media.api-sports.io/football/teams/2814.png"),
    "metropolitanos-fc": Team(id=2825, nombre="Metropolitanos FC", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/2825.png"),
    "puerto-cabello": Team(id=2827, nombre="Puerto Cabello", liga_ids=(13,), logo_url="https://media.api-sports.io/football/teams/2827.png"),
    "u-catolica": Team(id=2994, nombre="U. Catolica", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/2994.png"),
    "aurora": Team(id=3637, nombre="Aurora", liga_ids=(13,), logo_url="https://media.api-sports.io/football/teams/3637.png"),
    "always-ready": Team(id=3700, nombre="Always Ready", liga_ids=(13, 11), logo_url="https://media.api-sports.io/football/teams/3700.png"),
    "bolivar": Team(id=3702, nombre="Bol\u00edvar", liga_ids=(13,), logo_url="https://media.api-sports.io/football/teams/3702.png"),
    "jorge-wilstermann": Team(id=3705, nombre="Jorge Wilstermann", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/3705.png"),
    "nacional-potosi": Team(id=3706, nombre="Nacional Potos\u00ed", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/3706.png"),
    "the-strongest": Team(id=3711, nombre="The Strongest", liga_ids=(13,), logo_url="https://media.api-sports.io/football/teams/3711.png"),
    "juventud-unida-univ": Team(id=3947, nombre="Juventud Unida Univ.", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/3947.png"),
    "comunicaciones": Team(id=8008, nombre="Comunicaciones", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/8008.png"),
    "almirante-brown": Team(id=8375, nombre="Almirante Brown", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/8375.png"),
    "argentino-quilmes": Team(id=8376, nombre="Argentino Quilmes", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/8376.png"),
    "san-miguel": Team(id=8379, nombre="San Miguel", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/8379.png"),
    "el-porvenir": Team(id=8384, nombre="El Porvenir", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/8384.png"),
    "excursionistas": Team(id=8385, nombre="Excursionistas", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/8385.png"),
    "san-martin-burzaco": Team(id=8387, nombre="San Mart\u00edn Burzaco", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/8387.png"),
    "centro-espanol": Team(id=8390, nombre="Centro Espa\u00f1ol", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/8390.png"),
    "sportivo-ameliano": Team(id=10487, nombre="Sportivo Ameliano", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/10487.png"),
    "adt": Team(id=10492, nombre="ADT", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/10492.png"),
    "real-tomayapo": Team(id=15708, nombre="Real Tomayapo", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/15708.png"),
    "ciudad-de-bolivar": Team(id=16612, nombre="Ciudad de Bol\u00edvar", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/16612.png"),
    "rayo-zuliano": Team(id=16847, nombre="Rayo Zuliano", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/16847.png"),
    "universitario-de-vinto": Team(id=17762, nombre="Universitario de Vinto", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/17762.png"),
    "argentino-monte-maiz": Team(id=18764, nombre="Argentino Monte Ma\u00edz", liga_ids=(130,), logo_url="https://media.api-sports.io/football/teams/18764.png"),
    "deportivo-garcilaso": Team(id=20960, nombre="Deportivo Garcilaso", liga_ids=(11,), logo_url="https://media.api-sports.io/football/teams/20960.png"),
}


def get_team(slug: str) -> Team | None:
    return TEAMS.get(slug)


def slug_for_id(team_id: int) -> str | None:
    for slug, team in TEAMS.items():
        if team.id == team_id:
            return slug
    return None


def preferred_league_id(team: Team) -> int:
    if LIGA_PROFESIONAL in team.liga_ids:
        return LIGA_PROFESIONAL
    return team.liga_ids[0]


def preferred_league_name(team: Team) -> str:
    return COMPETICION_NOMBRES[preferred_league_id(team)]


def list_teams() -> list[dict]:
    return [
        {
            "nombre": team.nombre,
            "slug": slug,
            "escudo": team.logo_url,
            "competencia": preferred_league_name(team),
        }
        for slug, team in sorted(TEAMS.items(), key=lambda item: item[1].nombre)
    ]
