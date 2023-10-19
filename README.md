# Homework Pagerank

## Le groupe
Notre groupe est composé de 3 étudiants de master 2 en ALMA à Nantes Université :
* Quentin Gomes Dos Reis
* Rodrigue Meunier
* Matthéo Lécrivain

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
[google cloud plateform ](https://cloud.google.com).
Pour cela nous possédons plusieurs ressources à notre disposition :
* 50$ de crédit sur google cloud pour nous permettre de créer et d'utiliser des clusters sur le cloud
* Une implémentation de pagerank en pig
* Une implémentation de pagerank en spark

## Résultats
### Le plus grand pagerank

### Comparaisons

## Licence

