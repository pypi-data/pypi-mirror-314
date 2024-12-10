# ReprRW

## FRANÇAIS

Cette bibliothèque écrit la représentation d'objets Python dans un fichier
texte et lit le fichier pour recréer les objets. Une représentation d'objet
est une chaîne de caractères renvoyée par la fonction `repr`.

### Contenu

La fonction `write_reprs` écrit la représentation d'objets Python dans un
fichier texte. Chaque ligne du fichier est une représentation d'objet. Si le
fichier spécifié existe déjà, cette fonction l'écrase.

Le générateur `read_reprs` lit un fichier texte contenant des représentations
d'objet Python dans le but de recréer ces objets. Chaque ligne du fichier doit
être une représentation d'objet. Les lignes vides sont ignorées. Chaque
itération de ce générateur produit un objet.

Consultez la documentation des fonctions et les démos dans le dépôt de code
source pour plus d'informations.

### Dépendances

Installez les dépendances avec cette commande.
```
pip install -r requirements.txt
```

### Démos

Le script `demo_write.py` montre comment utiliser la fonction `write_reprs`. Il
faut l'exécuter en premier, car il produit un fichier dont `demo_read.py` a
besoin.

```
python demos/demo_write.py
```

Le script `demo_read.py` montre comment utiliser la fonction `read_reprs`. Il
faut l'exécuter après `demo_write.py`, car il ne fonctionne pas sans le fichier
produit par cet autre script.

```
python demos/demo_read.py
```

## ENGLISH

This library writes Python object representations in a text file and reads the
file to recreate the objects. An object representation is a string returned by
function `repr`.

### Content

Function `write_reprs` writes the representation of Python objects in a text
file. Each line in the file is an object representation. If the specified file
already exists, this function overwrites it.

Generator `read_reprs` reads a text file that contains the representation of
Python objects in order to recreate those objects. Each line in the file must be
an object representation. Empty lines are ignored. Each iteration of this
generator yields one object.

Consult the functions' documentation and the demos in the source code
repository for the complete information.

### Dependencies

Install the dependencies with this command.
```
pip install -r requirements.txt
```

### Demos

Script `demo_write.py` shows how to use function `write_reprs`. It must be
executed first because it makes a file that `demo_read.py` needs.

```
python demos/demo_write.py
```

Script `demo_read.py` shows how to use function `read_reprs`. It must be
executed after `demo_write.py` because it cannot work without the file made by
that other script.

```
python demos/demo_read.py
```
