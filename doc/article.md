# Cartography and Analysis of Sports Facilities in Africa through OpenStreetMap

---

## Abstract

**Context** – Africa does not have a consolidated continent-wide database of sports facilities. Yet, the distribution of sports infrastructure is a valuable indicator of territorial practices, historical legacies, and social inequalities.  

**Objectives** – This article offers a cartographic and critical reading of African sports infrastructure using open data from OpenStreetMap (OSM). It aims to assess their volume, spatial distribution, typology by sport, and to explore the historical dimension of certain sporting practices.  

**Methods** – Using the Africa OSM extract (2025 version), an automated workflow was applied to extract, filter, and geolocate more than 110,000 sports sites through Python scripts and tools such as **osmium** and **GeoPandas**. Interactive visualizations were produced with Folium, and a thematic classification of sports was carried out.  

**Results** – Football largely dominates, but less visible sports such as **netball** or **bowls** are very present in certain territories. The maps reveal a strong correlation between the presence of certain sports (cricket, rugby, hockey) and former Commonwealth territories, while these disciplines are nearly absent from ex-French colonies.  

**Conclusion** – These results show that sport is a meaningful marker of social and geopolitical dynamics in Africa. Open data enables the establishment of an evolving observatory, reflecting both the legacies and transformations of sport across the continent.  

**Keywords**: OpenStreetMap, sport, Africa, territory, netball, Commonwealth  

---

## Introduction

Recognizing that no consolidated, continent-wide dataset currently exists on the number, distribution, and types of sports facilities in Africa, this article proposes an exploratory approach based on **free and open data from OpenStreetMap (OSM)**. In a context where the visibility of sports policies varies greatly between states and regions, and where infrastructures are sometimes absent from official statistics, this collaborative database allows us to draw a first transversal cartography of places identified as sporting by contributors.  

This attempt at census through citizen-generated data is not intended to be exhaustive or fully representative: certain facilities—particularly informal football fields, widespread in urban and rural areas—are not always mapped. Coverage biases are also expected depending on the region and the density of the local OSM community. Nevertheless, the method provides a solid starting point to identify trends, monitor development dynamics, and above all lay the foundations for a **reproducible observatory** over time.  

This analysis focuses on three main dimensions:  

1. The **volume and geographic distribution** of sports facilities recorded in 2025 on the African continent via OSM;  
2. Their **distribution by type of sport**, allowing observation of implicit hierarchies and territorial preferences;  
3. The exploration of a **legacy**, particularly the persistence of “British” sports in territories historically linked to the Commonwealth.  

---

## 1. Methodological Approach and Use of Open Data

### 1.1 OpenStreetMap and Open Data: A Collaborative Citizen-Led Cartography

In a continental context marked by heterogeneity and the absence of a consolidated database of sports infrastructures, open data provides a valuable opportunity to produce a renewed view of the territorialization of sport. Among the most accessible and dynamic sources is **OpenStreetMap (OSM)**, a collaborative mapping project launched in 2004, based on contributions from thousands of volunteers worldwide.  

OSM is more than an open alternative to institutional cartographic systems: it is a collective work grounded in field logic. Mapped objects (roads, buildings, activity areas, places of worship, or sports facilities) are geolocated and described by standardized **tags**, allowing thematic extractions. For sports facilities, contributors use labels such as `leisure=pitch`, `leisure=stadium`, `building=stadium` to designate function and nature, while the tag `sport=*` specifies the sport(s) played at the site.  

This participatory dimension makes OSM particularly relevant for studying sport in Africa, since many sporting spaces (informal pitches, municipal stadiums not listed) escape official databases but can be identified and shared by local actors. OSM thus becomes a **citizen observatory**, evolving and capable of reflecting often invisible territorial realities.  

However, this richness comes with limitations: uneven coverage depending on the area, variable metadata quality, blurred local denominations, and good-faith approximations in mapping. Hence, a **critical and rigorous** treatment of the data is required to yield a meaningful reading at continental scale.  

### 1.2 Building the Dataset and Processing Sports Information

Given the absence of centralized data on African sports facilities, we carried out a **systematic extraction** from OSM data available in `.pbf` format on the [Geofabrik portal](http://download.geofabrik.de/africa.html), updated on **20 March 2025**.  

Processing took place in several steps (see code in Appendix):  

- **Filtering** spatial objects with tags `leisure=pitch`, `leisure=stadium`, `building=stadium`, plus an explicit `sport=*`, using the `osmium` command-line tool.  
- **Conversion** to GeoJSON for easier handling with Python libraries such as **GeoPandas**.  
- **Selection** of relevant entities, with extraction of geometries (coordinates) and recorded sport types.  
- **Cleaning**: removal of duplicates, filtering of entries without specified sport, and normalization of sport names.  

Particular attention was given to **multiple sports declared** for the same facility, common in OSM (e.g. `football;basketball`). To avoid counting bias, a decomposition step split these into one record per sport. This produced a structured CSV file [`sports_facilities.csv`](csv/sports_facilities), containing more than **113,000** sites across the continent.  

This reproducible and automatable process allows for regular updates of the analysis and observation of changes in African sports infrastructures over time. It also opens the way to comparative readings between territories, to the identification of emerging dynamics, and to highlighting possible symbolic hierarchies of disciplines depending on geographic distribution. Comparisons with the past are also possible using archived OSM dumps (e.g., 2020, 2015).  

---

## 2. Visualization and Distribution of Sports Facilities in Africa

The use of OSM data is not limited to simple counts. One of the strengths of this approach lies in its **spatial dimension**: each sports site is associated with a precise geographic location. This geovisual potential was used to produce an **interactive online map**, where each point corresponds to an identified facility, regardless of size or use. The aim is twofold: to make visible the continental distribution of sporting places and to enable qualitative exploration through tooltips showing the recorded sport.  

### 2.1 An Interactive and Zoomable Map of Sports Facilities

The interactive map was generated from the filtered CSV file, converted into a geographic object with GeoPandas, and displayed using the **Folium** library, which exports a dynamic HTML map.  

Each point represents a sports facility identified in OSM, with a tooltip showing the sport(s) played. The map can be zoomed to the local scale, enabling exploration of large sporting agglomerations (Lagos, Johannesburg, Nairobi, Accra…) as well as rural or isolated areas. A first visual reading already shows:  

- A strong concentration of facilities around **national capitals** and **regional metropolises**.  
- Marked disparities between **coastal regions** and **Sahelian or landlocked** areas.  
- Isolated points in poorly covered territories, revealing unequal OSM contributions.  

### 2.2 Distribution of Sports and Football’s Predominance

In parallel with this geographic reading, a statistical analysis of the frequency of reported sports was conducted. From (`sports_facilities.csv`)[csv/sports_facilities.csv], exploding multi-sport entries produced (`sport_counts.csv`)[csv/sports_count.csv], containing the number of facilities per discipline.  

| OSM tag       | Interpreted sport           | Number of sites |
|---------------|-----------------------------|-----------------|
| `soccer`      | Football (soccer)           | 55,487          |
| `tennis`      | Tennis                      | 24,229          |
| `basketball`  | Basketball                  | 9,986           |
| `multi`       | Multi-sport / Multipurpose  | 7,012           |
| `netball`     | Netball                     | 3,377           |
| `golf`        | Golf                        | 1,869           |
| `volleyball`  | Volleyball                  | 1,642           |
| `cricket`     | Cricket                     | 1,389           |
| `bowls`       | Lawn bowls                  | 1,137           |
| `handball`    | Handball                    | 1,133           |
| `football`    | Football (ambiguous)        | 854             |
| `field_hockey`| Field hockey                | 772             |
| `rugby_union` | Rugby union                 | 727             |
| `athletics`   | Athletics                   | 672             |
| `equestrian`  | Equestrian                  | 655             |
| `boules`      | Boules / Pétanque           | 438             |
| `beachvolleyball` | Beach volleyball        | 379             |
| `baseball`    | Baseball                    | 376             |
| `rugby`       | Rugby (unspecified)         | 371             |
| `shooting`    | Shooting                    | 348             |
| `padel`       | Padel                       | 327             |
| `running`     | Running                     | 297             |
| `skateboard`  | Skateboard                  | 282             |
| `futsal`      | Futsal                      | 248             |

The results unsurprisingly show the predominance of football, which alone accounts for over 50% of tagged facilities. It is followed by tennis, basketball, volleyball, and rugby. Netball ranks surprisingly high with more than **3,300** sites.  

---

## 3. Cultural and Geopolitical Analysis of Sports Distribution

The cartographic and statistical analysis of sports facilities from OSM allows us not only to measure territorial inequalities of access but also to develop cultural and geopolitical hypotheses about distribution. Certain practices, though invisible in global sports narratives, prove to be strongly rooted in specific regions, often linked to shared colonial histories.  

### 3.1 The Singular Case of Netball: A Minor Sport with Major Rank

Netball ranks fifth in the recorded sports list (3,377 sites), ahead of globally prominent disciplines like volleyball, cricket, or rugby. This may be surprising, since the sport is relatively unknown outside a few contexts. Originating from a British educational adaptation of basketball, netball is especially practiced in **Commonwealth anglophone countries**, particularly among women, in school and community contexts.  

The spatial analysis shows a strong concentration in **East and Southern Africa**—Kenya, South Africa, Malawi, Zimbabwe—precisely the areas where the British colonial legacy integrated the sport into education policies. In contrast, francophone and lusophone countries record almost no netball facilities.  

This case shows how some sports, although absent from mainstream media or international competitions, can occupy a **structuring territorial role**, acting as powerful identity markers at local or regional levels.  

### 3.2 British Sports and Commonwealth Territories: The Weight of the Past

Other sports historically tied to British culture—**cricket, rugby union, field hockey, bowls**—confirm this geography of sport. Crossing OSM facility locations with former colonial areas highlights strong patterns:  

- **Rugby**, although popular in France, is weakly represented in francophone OSM data. Conversely, it is well established in Commonwealth countries such as **South Africa, Namibia, Kenya, Zimbabwe, Uganda**, which account for most of the 727 `rugby_union` records.  
- **Cricket** shows an even clearer pattern, concentrated in **Nigeria, Ghana, Kenya, and South Africa**, and almost absent in francophone states.  
- **Field hockey**, an emblematic Olympic sport in Commonwealth countries, follows a similar distribution.  
- **Bowls** remains specific to anglophone Southern Africa.  

An interactive cartographic representation shows these distributions, with colors for each sport:  
- Field hockey in **red**  
- Cricket in **green**  
- Rugby in **blue**  
- Bowls in **purple**  

Far from being just places of physical exercise, mapped facilities express **long-term histories**, **differentiated education systems**, and enduring forms of cultural hegemony. Sport thus appears as a **silent yet structuring vector** of Africa’s post-imperial territorialities.  

---

## Conclusion

This work provides a first geographic reading of sports facilities in Africa using open OSM data. Through a reproducible methodology and collaborative data processing, it offers an unprecedented continental-scale overview of places identified as sporting by OSM contributors.  

Three key findings emerge:  

1. **Football** dominates African sporting space as mapped, confirming its central role in practices and imaginaries.  
2. Certain disciplines of low international visibility, such as **netball**, show strong footholds in specific territories, reflecting colonial educational and social continuities.  
3. Cross-analysis of cultural areas, former empires, and British-origin sports highlights a differentiated geography of sport in Africa, where infrastructures act as **implicit markers** of post-imperial territorialities.  

This study does not intend to close a debate, but to **open a field of research**. Using OSM not only makes evolving cartographies possible but also allows the conception of a **dynamic observatory of sport in Africa**, regularly updated, comparable over time (via older OSM dumps such as 2015, 2020), and cross-referenced with other datasets (demographic, climatic, linguistic, political).  

By revealing sports facilities as named and inscribed on the map by contributors—local or international—this approach brings into tension the **invisible and the visible, the popular and the elite, the present and the inherited pasts**.  

---

## Methodological Appendix: Extraction and Initial Processing of OSM Data

The following steps were used to build the corpus analyzed in this article:  

**Download OSM data for Africa (Geofabrik)**  
```bash
sudo wget -c -O /mnt/disk50/africa-latest.osm.pbf http://download.geofabrik.de/africa-latest.osm.pbf
```

**Filter relevant entities with osmium**  
```bash
osmium tags-filter africa-latest.osm.pbf     nwr/leisure=pitch nwr/leisure=stadium nwr/building=stadium     --overwrite -o filtered_data.osm
```

**Convert to GeoJSON**  
```bash
osmium export filtered_data.osm -f geojson --overwrite -o temp.geojson
```

**Data processing in Python (example)**  
```python
import geopandas as gpd
gdf = gpd.read_file("temp.geojson")
gdf_filtered = gdf[gdf["sport"].notna()][["geometry", "sport"]]
gdf_filtered.to_csv("sports_facilities.csv", index=False)
```

**Statistical analysis by discipline**  
```python
import pandas as pd
df = pd.read_csv("sports_facilities.csv")
df_exploded = df.assign(sport=df["sport"].str.split(";")).explode("sport")
sport_counts = df_exploded["sport"].value_counts()
sport_counts.to_csv("sport_counts.csv", header=["count"])
```
