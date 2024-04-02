# Algorama
Traduis / execute un algorithme en Python

## Installation

pour installer la librairie algorama, il de copier les ficher dans votre répertoire de travail ou avec la commande suivante:

```bash
git clone https://github.dev/AZachia/algorama.git && cd algorama
```

## Utilisation

algorama s'utilise en ligne de commande:

```bash
python algorama.py  <fichier>
```

### executer un fichier d'algorithme:

```bash
python algorama.py  <fichier>
```
ou
    
```bash
python algorama.py  <fichier> -r
```
ou
    
```bash
python algorama.py  <fichier> -run
```

### traduire un fichier d'algorithme:

```bash
python algorama.py  <fichier> -s
```

ou

```bash
python algorama.py  <fichier> -s -o <fichier_sortie>
```

## Documentation de l'algorithme

### Structure de l'algorithme

```py
Début
    #code ici
    afficher "Hello World"
    Fin
```

### Les variables

```py
Début
    var1 <- 10
    var2 <- 20
    var3 <- var1 + var2
    afficher var3
    Fin
```

### Les conditions

```py
Début
    var1 <- 10
    var2 <- 20
    Si var1 > var2:
        afficher "var1 est plus grand que var2"
        FinSi
    Sinon
        afficher "var2 est plus grand que var1"
        FinSinon
    Fin
```

### Les boucles

boucle pour:
```py
Début
    Pour i de 1 à 10:
        afficher i
        FinPour
    Fin
```
boucle tant que:
```py
Début
    i <- 1
    TantQue i < 10:
        afficher i
        i <- i + 1
        FinTantQue
    Fin
```

### Les fonctions

```py

Début
    Fonction somme:
        variables:
            a
            b
            FinVariables
        Algo:
            somme <- a + b
            retourner somme
            FinAlgo
    
    resulat <- executer somme 10, 20
    afficher "10 + 20 =", resulat
```

## Importer des algorithmes

```py
# importer tout de fichier.algo
utiliser fichier

Début
    afficher "Hello World"
    Fin
```