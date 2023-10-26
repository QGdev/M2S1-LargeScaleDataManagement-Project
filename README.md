# Homework Pagerank

## Le groupe
Notre groupe est composé de 3 étudiants de master 2 en ALMA à Nantes Université :
* [Quentin Gomes Dos Reis](https://github.com/QGdev)
* [Rodrigue Meunier](https://github.com/Rod4401)
* [Matthéo Lécrivain](https://github.com/MattheoLec)

## Sujet
Le sujet est disponible sur [madoc](https://madoc.univ-nantes.fr/mod/assign/view.php?id=1952911).
Voici une copie : 
```
Bonjour,

Je veux avoir une comparaison des performances sur pagerank, entre une implantation Pig et une implantation PySpark (Comme dans la vidéo NDSI 2012).

Je veux plusieurs configurations de cluster -> 1 noeuds, 2 noeuds, 4 noeuds (mais gardez le même hardware CPU/RAM par noeud , sinon les résultats ne sont pas comparables).

Les données sont dans: gs:///public_lddm_data/

Mes code sources sont dispos à: https://github.com/momo54/large_scale_data_management

Les résultats doivent être présentés sur un github ou gitlab avec le code source et les résultats d'exp dans le README. Je veux voir quelle est l'entité avec le plus grand page rank :).

Le rendu est donc une URL.

Faites attention au positionnement des données (voir l’article NSDI), je veux que vous évitiez le shuffle pour pagerank/neighbours.
```
## Description du projet
L'objectif de ce travail consiste à évaluer les performances de l'algorithme de pagerank entre la version pig et spark sur 
[Google Cloud Plateform ](https://cloud.google.com).
Pour cela nous possédons plusieurs ressources à notre disposition :
* 50$ de crédit sur google cloud pour nous permettre de créer et d'utiliser des clusters sur le cloud
* Une implémentation de pagerank en pig
* Une implémentation de pagerank en spark


## Résultats

### Les scripts bash utilisés
Tous les scripts sont présent dans le dossier scripts.
Le dossier contient :
* [pig.sh](https://github.com/QGdev/M2S1-LargeScaleDataManagement-Project/blob/main/scripts/pig.sh) : Contient le code permettant de créer un cluster et d'executer pagerank avec [Pig](https://fr.wikipedia.org/wiki/Apache_Pig)
* [spark.sh](https://github.com/QGdev/M2S1-LargeScaleDataManagement-Project/blob/main/scripts/spark.sh) : Contient le code permettant de créer un cluster et d'executer pagerank avec [Spark](https://fr.wikipedia.org/wiki/Apache_Spark)
* [snakefile](https://github.com/QGdev/M2S1-LargeScaleDataManagement-Project/blob/main/scripts/snakefile) : Contient le code [Snakemake](https://snakemake.readthedocs.io/en/stable/index.html) permettant d'opérer toutes les executions et de reprendre si échec pour éviter de perdre toutes les données obtenues.

### Benchmarks

#### Pig
| Nombre de workers | Tps d'exécution  
| ------------- | -------------|
| 2 | 49min 2s 450ms <br> ~2942450 ms |
| 3 | xxx |
| 4 | xxx |
| 5 | 33min 12s 746ms <br> ~1992746 ms  |
#### Spark
| Nombre de workers | Tps d'exécution  
| ------------- | -------------|
| 2 | 43min 39s 800ms <br> ~2619800 ms |
| 4 | 37min 41s 762ms  <br> ~2261762 ms |
| 5 | xxx |

#### Spark "optimisé"
| Nombre de workers | Tps d'exécution  
| ------------- | -------------|
| 2 | xxx |
| 3 | xxx |
| 4 | xxx |
| 5 | 36min 52s 253ms  <br> ~2212253 ms |

### La meilleure techno
| Rank | Tps d'exécution | Techno |
| ------------- | -------------| -------------|
| 1 | xxx | pig/spark |
| 2 | xxx | pig/spark |
| 3 | xxx | pig/spark |

### Le plus grand pageRank

Donc la page dbPedia qui est la plus référencée est : 

### Comparaisons

## Licence

