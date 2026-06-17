"""Fonctions partagées pour l'analyse des équipements sportifs (OSM Afrique).

Toute la chaîne de traitement repose sur le fichier ``data/sports_facilities.csv``
(colonnes ``geometry`` au format WKT, ``sport`` au format brut OSM).
"""

from __future__ import annotations

from pathlib import Path

from shapely.wkt import loads

# Racine du dépôt (ce fichier vit dans scripts/).
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DOCS_DIR = ROOT / "docs"
FACILITIES_CSV = DATA_DIR / "sports_facilities.csv"

# Date de l'extrait Geofabrik utilisé pour figer l'étude.
SNAPSHOT_DATE = "2026-06-15"

# Séparateur officiel des valeurs multiples du tag sport dans OSM.
SPORT_SEPARATOR = ";"

# Normalisation de la longue traîne : fautes de frappe, casse, variantes
# linguistiques regroupées vers le tag OSM canonique.
SPORT_ALIASES = {
    "socer": "soccer",
    "soccer.": "soccer",
    "footbal": "soccer",
    "foot-ball": "soccer",
    "foot_ball": "soccer",
    "football_ground": "soccer",
    "association_football": "soccer",
    "fútbol": "soccer",
    "futbol": "soccer",
    "beachsoccer": "beach_soccer",
    "futbol_playa": "beach_soccer",
    "basket": "basketball",
    "basket_ball": "basketball",
    "tenis": "tennis",
    "lawn tennis court": "tennis",
    "volley-ball": "volleyball",
    "beeachvolleyball": "beachvolleyball",
    "balonmano_playa": "beach_handball",
    "team_handball": "handball",
    "wresling": "wrestling",
    "athletisme": "athletics",
    "atheletics": "athletics",
    "petanque": "boules",
    "petanca": "boules",
    "lawn_bowls": "bowls",
    "nezball": "netball",
    "nedball": "netball",
    "rugby_league": "rugby_league",
    "lutte": "wrestling",
    "karate": "martial_arts",
    "karaté": "martial_arts",
    "judo": "martial_arts",
    "taekwondo": "martial_arts",
    "boxe": "boxing",
}

# Sports historiquement liés à la culture britannique / au Commonwealth,
# utilisés pour l'analyse géopolitique.
BRITISH_SPORTS = {
    "field_hockey": {"label": "Hockey sur gazon", "color": "#e63946"},
    "cricket": {"label": "Cricket", "color": "#2a9d8f"},
    "rugby_union": {"label": "Rugby à XV", "color": "#1d3557"},
    "bowls": {"label": "Boulingrin (bowls)", "color": "#7209b7"},
}

# Libellés français des principaux tags pour l'affichage.
SPORT_LABELS = {
    "soccer": "Football",
    "tennis": "Tennis",
    "basketball": "Basketball",
    "multi": "Multi-sport",
    "netball": "Netball",
    "golf": "Golf",
    "volleyball": "Volley-ball",
    "cricket": "Cricket",
    "bowls": "Boulingrin (bowls)",
    "handball": "Handball",
    "football": "Football (ambigu)",
    "field_hockey": "Hockey sur gazon",
    "rugby_union": "Rugby à XV",
    "athletics": "Athlétisme",
    "equestrian": "Équitation",
    "boules": "Boules / Pétanque",
    "beachvolleyball": "Beach-volley",
    "baseball": "Baseball",
    "rugby": "Rugby (non spécifié)",
    "shooting": "Tir sportif",
    "padel": "Padel",
    "running": "Course à pied",
    "skateboard": "Skateboard",
    "futsal": "Futsal",
}


def normalize_sport(raw: str) -> str | None:
    """Nettoie un tag sport OSM brut vers une forme canonique.

    Retourne ``None`` pour les valeurs vides ou clairement non pertinentes.
    """
    if raw is None:
        return None
    token = str(raw).strip().lower()
    if not token:
        return None
    # Bruit manifeste à écarter.
    if token in {"yes", "no", "all", "*", "q", "qq", "mm", "co", "aaaa", "unknown"}:
        return None
    return SPORT_ALIASES.get(token, token)


def explode_sports(series):
    """Décompose les valeurs multiples (``a;b``) en un sport canonique par ligne."""
    exploded = (
        series.fillna("")
        .str.split(SPORT_SEPARATOR)
        .explode()
        .map(normalize_sport)
        .dropna()
    )
    return exploded


def extract_point(geom_str):
    """Extrait un couple (latitude, longitude) représentatif d'une géométrie WKT."""
    try:
        geom = loads(geom_str)
    except Exception:
        return None, None
    if geom.is_empty:
        return None, None
    if geom.geom_type == "Point":
        return geom.y, geom.x
    if geom.geom_type == "LineString":
        mid = geom.interpolate(0.5, normalized=True)
        return mid.y, mid.x
    # Polygon, MultiPolygon, etc. : on prend le centroïde.
    c = geom.centroid
    return c.y, c.x
