# Construire les données manquantes à l'échelle continentale : une méthode reproductible à partir d'OpenStreetMap

## *Étude de cas : les équipements sportifs en Afrique via OpenStreetMap (2026)*

Benoît Prieur  
 ORCID: 0000-0003-0786-0049

# **Résumé**

À l'échelle transnationale, et plus encore à l'échelon continental, les données ouvertes sont rarement harmonisées et comparables. Lorsqu'elles existent (comme dans certaines régions, en Europe notamment), elles demeurent le plus souvent produites, financées et publiées à l'échelon national, si bien qu'aucune base cohérente ne se constitue au-dessus des frontières. De nombreux objets d'intérêt public se retrouvent ainsi sans recensement ouvert dès que l'on change d'échelle. 

Une réponse consiste à reconstruire cette donnée à partir de sources citoyennes mondiales comme OpenStreetMap (OSM), à condition d'en expliciter les limites. L'intérêt est triple : obtenir une première mesure géolocalisée là où aucun chiffre n'existait, comparer des territoires que les statistiques officielles ne reliaient pas, et, la chaîne étant reproductible, suivre l'évolution dans le temps. 

Nous appliquons cette démarche aux équipements sportifs en Afrique, domaine dépourvu de recensement continental ouvert. À partir de l'extrait Afrique de Geofabrik (15 juin 2026), une chaîne automatisée (osmium, Python, Folium) filtre, géolocalise et normalise 123 936 sites, soit 126 928 occurrences de sport réparties en 194 disciplines. Le football domine (61 679 sites), mais des disciplines moins médiatisées ressortent localement, comme le netball (cinquième rang, 3 821 sites). 

Surtout, à l'échelle du continent, la répartition du cricket, du rugby à XV et du hockey sur gazon recoupe nettement les anciennes aires coloniales britanniques (motif transnational qu'aucune statistique nationale ne révélerait), ces sports étant quasi absents des espaces francophones et lusophones. Imparfaite et non représentative, la donnée OSM offre néanmoins un point d'entrée robuste et reproductible à l'échelle continentale.

Mots-clés : OpenStreetMap, données ouvertes, échelle continentale, information géographique volontaire, équipements sportifs, Afrique, reproductibilité, Commonwealth.

# **Abstract**

At the transnational scale, and even more so at the continental level, open data are rarely harmonized and comparable. Where they do exist (as in some regions, notably Europe), they remain most often produced, funded, and published at the national level, so that no coherent dataset emerges above borders. Many objects of public interest are thus left without any open inventory as soon as the scale changes.

One response consists in reconstructing this data from global citizen sources such as OpenStreetMap (OSM), provided that its limitations are made explicit. The benefit is threefold: obtaining a first geolocated measurement where no figure previously existed, comparing territories that official statistics did not connect, and—since the pipeline is reproducible—tracking change over time.

We apply this approach to sports facilities in Africa, a field lacking any open continental inventory. Starting from the Geofabrik Africa extract (15 June 2026), an automated pipeline (osmium, Python, Folium) filters, geolocates, and normalizes 123,936 sites, amounting to 126,928 sport occurrences spread across 194 disciplines. Football dominates (61,679 sites), but less prominent disciplines stand out locally, such as netball (fifth rank, 3,821 sites).

Above all, at the continental scale, the distribution of cricket, rugby union, and field hockey clearly overlaps with the former British colonial areas (a transnational pattern that no national statistic would reveal), these sports being almost absent from French- and Portuguese-speaking spaces. Although imperfect and non-representative, OSM data nonetheless provide a robust and reproducible entry point at the continental scale.

Keywords: OpenStreetMap, open data, continental scale, volunteered geographic information, sports facilities, Africa, reproducibility, Commonwealth.

# 

# **Introduction**

De nombreux domaines ne disposent d'aucune source ouverte, harmonisée et comparable à l'échelle transnationale. L'enquête s'y interrompt souvent faute de matériau. Il reste possible de reconstruire une donnée à partir de sources déjà disponibles, en particulier les contributions citoyennes mondiales, dès lors que l'on en explicite les limites. La donnée obtenue par cette voie demeure une approximation. Sa couverture est partielle, ses métadonnées sont hétérogènes et sa production reflète des biais de contribution. Elle présente en retour des propriétés rares pour ce type d'objet, puisqu'elle est ouverte, géolocalisée, mondiale et reproductible.

Cet article applique la démarche aux équipements sportifs en Afrique. Il n'existe pas, à l'échelle du continent, de recensement officiel, harmonisé et ouvert de ces infrastructures. Les statistiques disponibles restent nationales, éparses, rarement géolocalisées et souvent inaccessibles. Cette lacune renseigne sur la faible institutionnalisation de la donnée sportive et sur les angles morts de l'open data.

La source retenue est OpenStreetMap (OSM), projet de cartographie collaborative lancé en 2004[^1]. OSM agrège les contributions de centaines de milliers de bénévoles et constitue un exemple documenté d'information géographique volontaire[^2]. Les contributeurs y décrivent terrains, stades et aires de jeu à l'aide de balises normalisées dont la documentation est publique, ce qui autorise des extractions thématiques à grande échelle.

Les limites de l'approche sont posées d'emblée. La donnée OSM n'est ni exhaustive ni représentative. Un terrain informel, fréquent en milieu urbain comme rural, échappe souvent au recensement, et la densité de contribution varie fortement d'un pays à l'autre[^3]. L'approche permet en contrepartie d'obtenir une première mesure géolocalisée là où aucun chiffre n'existait, de comparer des territoires que les statistiques officielles ne reliaient pas, et de suivre l'évolution dans le temps grâce à une chaîne reproductible.

L'analyse porte sur trois dimensions : le volume et la répartition géographique des équipements recensés en 2026, leur distribution par discipline, et la persistance des sports d'origine britannique dans les territoires historiquement liés au Commonwealth.

# **Partie 1\. Approche méthodologique**

## **1.1. OpenStreetMap comme source d'open data**

OpenStreetMap est une œuvre collective fondée sur l'observation de terrain, ouverte et indépendante des systèmes cartographiques institutionnels[^4]. Les objets qui y figurent, routes, bâtiments, lieux d'activité et infrastructures sportives, sont géolocalisés et décrits par des balises normalisées. Pour les équipements sportifs, les contributeurs mobilisent principalement leisure=pitch, leisure=stadium et building=stadium, le tag sport=\* précisant la ou les disciplines pratiquées[^5].

Cette dimension participative est ce qui rend la source pertinente là où la donnée officielle fait défaut, puisque des espaces sportifs absents des bases institutionnelles peuvent y être repérés et décrits par des acteurs locaux. Les contreparties sont connues : couverture inégale, qualité variable des métadonnées, dénominations locales imprécises et approximations de bonne foi. Elles imposent un traitement critique et une étape de nettoyage explicite. L'ensemble des données dérivées reste soumis à l'Open Database License[^6].

## **1.2. Construction et nettoyage du jeu de données**

L'extraction part de l'extrait continental au format .osm.pbf mis à disposition par Geofabrik, dans sa version du 15 juin 2026[^7]. Le traitement se déroule en plusieurs étapes : 

1. filtrage des objets portant leisure=pitch, leisure=stadium ou building=stadium à l'aide de l'outil en ligne de commande osmium[^8] ;  
2. conversion au format GeoJSON, puis extraction de la géométrie et du tag sport avec les bibliothèques Python pandas et shapely. Les géométries linéaires et surfaciques sont ramenées à un point représentatif, milieu de ligne ou centroïde ;  
3. décomposition des déclarations multiples. Un même site peut porter plusieurs disciplines, par exemple soccer;basketball. Le séparateur officiel « ; » sert à produire un enregistrement par sport ;  
4. normalisation de la longue traîne : harmonisation de la casse et des espaces, correction des fautes fréquentes (socer → soccer, volley-ball → volleyball, athletisme → athletics) et regroupement des variantes. Le tag générique football, que la documentation OpenStreetMap déconseille au profit de soccer, est rattaché à ce dernier. Cette étape ramène le nombre de tags distincts d'environ 250 à 194\.

Le corpus final comporte 123 936 sites et 126 928 occurrences de sport, un site pouvant en cumuler plusieurs. Le fichier brut est conservé intact (data/sports\_facilities.csv), de sorte que chaque choix de nettoyage demeure auditable et rejouable.

## **1.3. Une chaîne pensée pour l'évolution**

L'intérêt principal de cette méthode tient à sa reproductibilité, davantage qu'aux chiffres obtenus pour l'année 2026 elle-même. La chaîne étant entièrement automatisée et son code ouvert, elle se prête à deux usages temporels complémentaires. Le premier est prospectif : relancée sur l'extrait du mois ou de l'année suivante, elle produit une mesure directement comparable et transforme l'instantané isolé en série. Le second est rétrospectif : appliquée aux archives d'OpenStreetMap, en particulier aux versions à historique complet (full-history dumps), elle permet de reconstituer une trajectoire passée et de dater l'apparition des sites. Dans les deux cas, la donnée gagne une profondeur que ne possède aucun recensement ponctuel : densification de la contribution, émergence de nouvelles disciplines comme le padel ou le pickleball, dynamique d'équipement de certaines régions.

Cette comparabilité dans le temps n'est toutefois acquise que sous conditions, qui relèvent elles aussi de la méthode. Deux instantanés ne sont rapprochables que si l'on conserve à l'identique les filtres d'extraction (leisure=pitch, leisure=stadium, building=stadium), la table de normalisation des disciplines et le périmètre géographique, et si chaque exécution est rattachée à une date d'extrait explicite. C'est la raison pour laquelle le fichier brut est gelé et versionné à chaque passage, et pour laquelle les règles de nettoyage sont décrites plutôt qu'appliquées de façon *ad hoc* : la stabilité du protocole prime sur l'optimisation ponctuelle d'un résultat.

Une limite, enfin, accompagne ce gain : toute variation observée entre deux dates mesure indissociablement l'évolution réelle de l'équipement et celle de l'activité contributive. Une hausse du nombre de sites peut traduire la construction de nouveaux terrains autant que le rattrapage cartographique d'une communauté OpenStreetMap plus active. C'est le pendant temporel du biais déjà relevé pour la carte de densité, et il invite à lire les séries comme des tendances structurelles plutôt que comme des décomptes absolus. Sous cette réserve, la démarche n'a rien de spécifique aux équipements sportifs : la même chaîne s'applique à tout objet d'intérêt public dépourvu de recensement continental ouvert, ce qui en fait moins un dénombrement qu'un observatoire reproductible.

# **Partie 2\. Résultats et lecture à l'échelle continentale**

## **2.1. Une géographie de la concentration**

Chaque site étant géolocalisé, une carte de densité a été produite avec Folium (figure 1). Sa lecture fait ressortir trois traits : 

1. la concentration est nette autour des capitales et des métropoles régionales comme Lagos, Johannesburg, Nairobi, Le Caire ou Accra ;  
2. les écarts sont marqués entre les façades littorales et les espaces sahéliens ou enclavés, moins équipés et moins cartographiés ;  
3. des points isolés apparaissent enfin dans des territoires faiblement couverts, où ils traduisent autant l'état réel de l'équipement que l'inégale activité des communautés OpenStreetMap locales.

![Carte de densité des équipements sportifs en Afrique](fig1_density.png)

Figure 1\. Densité des équipements sportifs recensés sur OpenStreetMap, continent africain, extrait Geofabrik du 15 juin 2026\. Données : © les contributeurs d'OpenStreetMap, sous licence ODbL.

Cette distribution doit donc se lire avec prudence. La carte superpose deux signaux, la présence effective d'équipements et l'intensité de la contribution bénévole, que la source ne permet pas de séparer entièrement. Elle indique des structures spatiales plus qu'elle ne fournit un dénombrement absolu.

## **2.2. Distribution par discipline et prédominance du football**

Une fois les déclarations multiples décomposées, le comptage par discipline fait apparaître une hiérarchie très contrastée (tableau 1). Le football concentre à lui seul près de la moitié des équipements étiquetés, devant le tennis et le basketball. Vient ensuite la catégorie générique multi, qui regroupe les sites polyvalents sans discipline unique déclarée. Le cinquième rang revient au netball, ce qui constitue le premier résultat inattendu et appelle une lecture culturelle développée plus loin.

| Valeur OSM | Sport interprété | Nombre de sites |
| ----- | ----- | ----- |
| soccer | Football | 61 679 |
| tennis | Tennis | 26 107 |
| basketball | Basketball | 10 774 |
| multi | Multi-sport / polyvalent | 7 557 |
| netball | Netball | 3 821 |
| golf | Golf | 1 835 |
| volleyball | Volley-ball | 1 786 |
| cricket | Cricket | 1 484 |
| handball | Handball | 1 290 |
| bowls | Boulingrin (bowls) | 1 238 |
| field\_hockey | Hockey sur gazon | 849 |
| rugby\_union | Rugby à XV | 827 |
| equestrian | Équitation | 809 |
| athletics | Athlétisme | 757 |
| padel | Padel | 552 |

Tableau 1\. Quinze disciplines les plus représentées, par nombre de sites (instantané 2026). Données : © les contributeurs d'OpenStreetMap, sous licence ODbL.

## **2.3. Le netball et les sports d'origine britannique : une empreinte du Commonwealth**

Le netball se classe au cinquième rang continental avec 3 821 sites, devant des disciplines mondiales comme le volley-ball, le cricket ou le rugby. Issu d'une adaptation du basketball dans le contexte éducatif britannique du début du XXe siècle, il est aujourd'hui surtout pratiqué dans les pays anglophones du Commonwealth, fréquemment par les femmes et en milieu scolaire[^9]. Sa présence sur le continent suit cette histoire. La carte dédiée (figure 2\) montre une concentration en Afrique de l'Est et australe, au Kenya, en Afrique du Sud, au Malawi et au Zimbabwe, là où l'héritage colonial britannique a inscrit ce sport dans les politiques d'éducation physique. Les espaces d'héritage francophone ou lusophone n'en présentent quasiment aucune occurrence.

![Carte de répartition des sites de netball en Afrique](fig2_netball.png)

Figure 2\. Répartition des sites de netball, continent africain (OpenStreetMap, extrait Geofabrik du 15 juin 2026). Données : © les contributeurs d'OpenStreetMap, ODbL.

Le même motif se retrouve, plus largement, pour d'autres disciplines historiquement liées à la culture britannique : le cricket, le rugby à XV (rugby\_union), le hockey sur gazon (field\_hockey) et le boulingrin (bowls). Le croisement de leurs localisations avec les anciennes aires coloniales fait apparaître des structures nettes. Le rugby, pourtant populaire en France, est peu présent dans les pays francophones du continent et se concentre en Afrique du Sud, en Namibie, au Kenya, au Zimbabwe et en Ouganda, qui rassemblent l'essentiel des 827 occurrences de rugby\_union. Le cricket suit une logique encore plus marquée, concentré en Afrique du Sud, au Kenya, au Nigéria et au Ghana, et presque absent des États francophones. Le hockey sur gazon se déploie selon une distribution comparable, et le boulingrin reste très spécifique de l'Afrique australe anglophone.

La carte thématique (figure 3\) associe une couleur à chacune de ces disciplines et fait coïncider leur empreinte avec les espaces du Commonwealth. Ces équipements renvoient à des histoires longues, à des systèmes éducatifs différenciés et à des formes durables d'influence culturelle. Le sport apparaît ainsi comme un marqueur discret mais structurant des territorialités post-impériales[^10]. Aucune statistique nationale agrégée ne rendrait visible ce motif transnational, que seule la mise en commun de données géolocalisées à l'échelle du continent permet de lire.

![Carte des sports d'origine britannique en Afrique : hockey sur gazon, cricket, rugby à XV, boulingrin](fig3_british_sports.png)

Figure 3\. Répartition du hockey sur gazon (rouge), du cricket (vert), du rugby à XV (bleu) et du boulingrin (violet), continent africain (OpenStreetMap, extrait Geofabrik du 15 juin 2026). Données : © les contributeurs d'OpenStreetMap, ODbL.

# 

# **Conclusion**

Cet article visait moins à dénombrer les équipements sportifs africains qu'à éprouver une méthode transposable : lorsqu'aucun recensement ouvert, harmonisé et comparable n'existe à l'échelle continentale, il reste possible de reconstruire une première donnée géolocalisée à partir de sources citoyennes mondiales comme OpenStreetMap, à la condition d'en expliciter les limites. Le sport sur le continent africain n'a ici valeur que d'exemple support : un domaine typiquement dépourvu de base continentale ouverte, sur lequel la démarche pouvait être déployée de bout en bout et auditée.

Appliqué à ce cas, le protocole a confirmé le triple intérêt annoncé. Il a d'abord produit une première mesure là où aucun chiffre n'existait, soit 123 936 sites et 126 928 occurrences réparties en 194 disciplines. Il a ensuite permis de comparer des territoires que les statistiques nationales ne reliaient pas : la concordance entre la répartition du cricket, du rugby à XV, du hockey sur gazon, du boulingrin et du netball, d'une part, et les anciennes aires coloniales britanniques, d'autre part, constitue un motif transnational qu'aucune source agrégée à l'échelon national n'aurait rendu visible. Il a enfin été pensé pour la comparaison dans le temps, puisque la chaîne entièrement automatisée transforme un instantané isolé en série potentielle.

Ces résultats valent dans les limites mêmes de la source, et les nommer fait partie de la méthode. La donnée OSM n'est ni exhaustive ni représentative ; la carte de densité superpose deux signaux difficilement séparables, la présence réelle d'équipements et l'intensité de la contribution bénévole. C'est précisément pourquoi le fichier brut est conservé intact et chaque opération de nettoyage rendue rejouable : la robustesse ne tient pas à l'exactitude du dénombrement, mais à la traçabilité et à la reproductibilité du procédé.

Au-delà du sport, c'est cette propriété qui mérite d'être retenue. La chaîne décrite ne dépend pas de l'objet recensé : elle peut s'appliquer à tout domaine d'intérêt public privé de recensement continental ouvert, et sa valeur croît avec le temps. Relancée sur les extraits successifs de Geofabrik ou sur les archives d'OpenStreetMap, elle donne accès à la densification de la contribution, à l'émergence de nouvelles disciplines comme le padel ou le pickleball, et à la dynamique d'équipement des régions. L'instantané de 2026 n'est ainsi qu'un point d'entrée : la donnée citoyenne, traitée avec méthode et lue avec prudence, peut alors fonctionner comme un observatoire reproductible à l'échelle d'un continent.

# **Annexe méthodologique** 

Téléchargement de l'extrait Afrique (Geofabrik) : 

| wget \-c \-O africa-latest.osm.pbf \\  https://download.geofabrik.de/africa-latest.osm.pbf |
| :---- |

Filtrage des entités pertinentes (osmium) : 

| osmium tags-filter africa-latest.osm.pbf \\  nwr/leisure=pitch nwr/leisure=stadium nwr/building=stadium \\  \--overwrite \-o filtered\_data.osm |
| :---- |

Conversion en GeoJSON : 

| osmium export filtered\_data.osm \-f geojson \--overwrite \-o temp.geojson |
| :---- |

Nettoyage, comptage et cartographie (voir scripts/ du dépôt) : 

| python scripts/build\_counts.pypython scripts/make\_map.py heatmappython scripts/make\_map.py sport \--sport netball \--color "\#1d3557" \--name netballpython scripts/make\_map.py british |
| :---- |

# **Bibliographie**

* Bale, J. & Cronin, M. (dir.) (2003). *Sport and Postcolonialism*. Oxford : Berg. [https://doi.org/10.4324/9781003086772](https://doi.org/10.4324/9781003086772)
* Geofabrik. *Africa: OpenStreetMap Data Extracts*. [https://download.geofabrik.de/africa.html](https://download.geofabrik.de/africa.html) (consulté en juin 2026).
* Goodchild, M. F. (2007). « Citizens as sensors: the world of volunteered geography ». *GeoJournal*, 69(4), 211-221. [https://doi.org/10.1007/s10708-007-9111-y](https://doi.org/10.1007/s10708-007-9111-y)
* Haklay, M. & Weber, P. (2008). « OpenStreetMap: User-Generated Street Maps ». *IEEE Pervasive Computing*, 7(4), 12-18. [https://doi.org/10.1109/MPRV.2008.80](https://doi.org/10.1109/MPRV.2008.80)
* Neis, P. & Zielstra, D. (2014). « Recent Developments and Future Trends in Volunteered Geographic Information Research: The Case of OpenStreetMap ». *Future Internet*, 6(1), 76-106. [https://doi.org/10.3390/fi6010076](https://doi.org/10.3390/fi6010076)
* OpenStreetMap. *Open Database License (ODbL)*. [https://www.openstreetmap.org/copyright](https://www.openstreetmap.org/copyright) (consulté en juin 2026).
* OpenStreetMap Foundation. *About OpenStreetMap*. [https://www.openstreetmap.org/about](https://www.openstreetmap.org/about) (consulté en juin 2026).
* OpenStreetMap Wiki. *Key:sport*. [https://wiki.openstreetmap.org/wiki/Key:sport](https://wiki.openstreetmap.org/wiki/Key:sport) (consulté en juin 2026).
* Osmium Tool. [https://osmcode.org/osmium-tool/](https://osmcode.org/osmium-tool/) (consulté en juin 2026).
* Wikipédia. « Netball », auteurs et historique (consulté en juin 2026), sous licence CC BY-SA. [https://fr.wikipedia.org/w/index.php?title=Netball\&action=history](https://fr.wikipedia.org/w/index.php?title=Netball&action=history)
* World Netball. *History of the game*. [https://netball.sport/](https://netball.sport/) (consulté en juin 2026).

[^1]: OpenStreetMap Foundation, *About OpenStreetMap*, [https://www.openstreetmap.org/about](https://www.openstreetmap.org/about) (consulté en juin 2026).

[^2]: Goodchild, M. F. (2007), « Citizens as sensors: the world of volunteered geography », *GeoJournal*, 69(4), 211-221, [https://doi.org/10.1007/s10708-007-9111-y](https://doi.org/10.1007/s10708-007-9111-y).

[^3]: Neis, P. & Zielstra, D. (2014), « Recent Developments and Future Trends in Volunteered Geographic Information Research: The Case of OpenStreetMap », *Future Internet*, 6(1), 76-106, [https://doi.org/10.3390/fi6010076](https://doi.org/10.3390/fi6010076).

[^4]: Haklay, M. & Weber, P. (2008), « OpenStreetMap: User-Generated Street Maps », *IEEE Pervasive Computing*, 7(4), 12-18, [https://doi.org/10.1109/MPRV.2008.80](https://doi.org/10.1109/MPRV.2008.80).

[^5]: OpenStreetMap Wiki, *Key:sport*, [https://wiki.openstreetmap.org/wiki/Key:sport](https://wiki.openstreetmap.org/wiki/Key:sport) (consulté en juin 2026).

[^6]: OpenStreetMap, *Open Database License (ODbL)*, [https://www.openstreetmap.org/copyright](https://www.openstreetmap.org/copyright) (consulté en juin 2026).

[^7]: Geofabrik, *Africa: OpenStreetMap Data Extracts*, [https://download.geofabrik.de/africa.html](https://download.geofabrik.de/africa.html) (consulté en juin 2026).

[^8]: *Osmium Tool*, [https://osmcode.org/osmium-tool/](https://osmcode.org/osmium-tool/) (consulté en juin 2026).

[^9]: World Netball, *History of the game*, [https://netball.sport/](https://netball.sport/) (consulté en juin 2026) ; Wikipédia, « Netball » (consulté en juin 2026), sous licence CC BY-SA.

[^10]: Bale, J. & Cronin, M. (dir.) (2003), *Sport and Postcolonialism*, Oxford, Berg, [https://doi.org/10.4324/9781003086772](https://doi.org/10.4324/9781003086772).