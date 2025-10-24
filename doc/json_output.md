# JSON OUTPUT - Comparatif des formats possibles

## 1. Format Matrice / Grille (Liste de listes)
Representing Matrices as JSON Objects - https://www.openriskmanagement.com/representing-matrices-as-json-objects-part-1/

Data Structure to Represent a Maze - https://stackoverflow.com/questions/4551575/data-structure-to-represent-a-maze


### Description
Un tableau 2D où chaque case correspond à un élément (mur, vide, bonus, etc.).
C’est le format le plus direct à générer en Python.

```json
{
  "width": 10,
  "height": 8,
  "grid": [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,1,0,1,0,1,0,1,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1]
  ],
  "legend": {
    "0": "vide",
    "1": "mur"
  }
}
```

### Analyse
* Lisibilité : correcte
* Facilité d’utilisation : excellente avec Pygame (chaque cellule est une tuile)
* Extensibilité : correcte (ajout de nouveaux codes possible)
* Taille du fichier : très légère

**Conclusion :** c’est le format le plus simple et le plus pratique pour un projet Pygame comme Pac-Man vu que chaque valeur correspond à une tuile graphique.

## 2. Format Liste d’objets (tuiles individuelles)
Real Python - Working with JSON Data in Python - https://realpython.com/python-json/

Stack Overflow - Practical way to create game levels/maps - https://stackoverflow.com/questions/19122730/most-practical-way-to-create-game-levelsmap


### Description

Chaque tuile est représentée par un objet JSON contenant ses coordonnées et son type.

```json
{
  "width": 10,
  "height": 8,
  "tiles": [
    {"x": 0, "y": 0, "type": "wall"},
    {"x": 1, "y": 0, "type": "wall"},
    {"x": 2, "y": 0, "type": "empty"}
  ]
}
```

### Analyse

* Lisibilité : bonne, chaque élément est compréhensible à la lecture
* Facilité d’utilisation : moyenne, nécessite de parcourir les objets pour reconstruire la grille
* Extensibilité : excellente, car on peut ajouter des propriétés (bonus, couleur, etc.)
* Taille du fichier : lourde sur de grandes cartes

**Conclusion :** utile pour ajouter des propriétés précises à chaque tuile, mais trop verbeux pour un grand labyrinthe et pas forcément nécessaire.


## 3. Format Tiled (éditeur de cartes 2D)
Tiled - JSON Map Format Documentation - https://doc.mapeditor.org/en/stable/reference/json-map-format/

### Description
C’est le format JSON utilisé par l’éditeur Tiled, un standard pour les jeux 2D basés sur des tuiles.
Une carte contient des couches (“layers”), des tilesets et des métadonnées comme la taille du niveau ou des tuiles.

```json
{
  "width": 28,
  "height": 31,
  "tilewidth": 32,
  "tileheight": 32,
  "layers": [
    {
      "name": "walls",
      "data": [
        1,1,1,1,1,1,1,1,1,1,
        1,0,0,0,0,0,0,0,0,1
      ]
    }
  ],
  "tilesets": [
    {"firstgid": 1, "source": "tileset.json"}
  ]
}
```

### Analyse

* Lisibilité : moyenne, car le format contient beaucoup de champs techniques
* Facilité d’utilisation : moyenne, il faut parser les couches avant affichage
* Extensibilité : très bonne, compatible avec plusieurs couches et propriétés personnalisées
* Taille du fichier : modérée

**Conclusion :** Très aboutit et détaillé, mais inutilement complexe, encore plus étant donné qu'on n'utilise pas l'éditeur tiled pour produire le json.
