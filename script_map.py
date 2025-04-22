import pandas as pd
import folium
from shapely.wkt import loads

# Charger les données depuis le CSV
CSV_FILE = "sports_facilities.csv"
df = pd.read_csv(CSV_FILE, names=["geometry", "sport"])

# Fonction pour extraire un point à partir de la géométrie
def extract_point(geom_str):
    try:
        geom = loads(geom_str)  # Convertir la géométrie WKT en objet Shapely
        
        if geom.geom_type == "Point":
            return geom.y, geom.x  # Latitude, Longitude
        elif geom.geom_type == "LineString":
            return geom.interpolate(0.5, normalized=True).y, geom.interpolate(0.5, normalized=True).x  # Milieu de la ligne
        elif geom.geom_type == "MultiPolygon":
            return geom.centroid.y, geom.centroid.x  # Centroïde du MultiPolygon
        else:
            print(f"⚠️ Géométrie non gérée : {geom.geom_type}")
            return None, None
    except Exception as e:
        print(f"⚠️ Erreur lors du parsing de la géométrie : {e}")
        return None, None

# Appliquer la fonction et filtrer les entrées valides
df["lat"], df["lon"] = zip(*df["geometry"].apply(extract_point))
df = df.dropna(subset=["lat", "lon"])  # Supprimer les lignes où lat/lon est None

# Vérifier un aperçu des données corrigées
print("\n✅ Données après extraction des points :")
print(df.head())

# Créer une carte centrée sur l'Afrique
m = folium.Map(location=[0, 25], zoom_start=3)

# Ajouter un point pour chaque site
for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=2,  # Taille du point
        color="red",
        fill=True,
        fill_color="red",
        fill_opacity=0.7,
        popup=row["sport"]  # Affiche le sport en popup
    ).add_to(m)

# Sauvegarde de la carte en HTML
m.save("sports_map.html")
print("\n✅ Carte générée : ouvre 'sports_map.html' dans un navigateur.")
