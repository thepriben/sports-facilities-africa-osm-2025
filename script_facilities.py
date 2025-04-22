import pandas as pd

# Charger le fichier CSV
CSV_FILE = "sports_facilities.csv"
df = pd.read_csv(CSV_FILE)

# Vérifier un aperçu des données
print("\n📌 Aperçu des 5 premières lignes :\n", df.head())

# Nombre total de sites (chaque ligne représente un site)
total_sites = len(df)
print(f"\n✅ Nombre total de sites : {total_sites}")

# Gérer les sports multiples en séparant les valeurs par ";"
df_exploded = df.assign(sport=df["sport"].str.split(";")).explode("sport")

# Compter le nombre de sites par sport
sport_counts = df_exploded["sport"].value_counts()

# Afficher la liste triée des sports par nombre de sites
print("\n📊 Nombre de sites par sport :\n")
print(sport_counts)

# Sauvegarde des résultats dans un CSV
sport_counts.to_csv("sport_counts.csv", header=["count"])
print("\n✅ Fichier 'sport_counts.csv' généré avec le nombre de sites par sport.")
