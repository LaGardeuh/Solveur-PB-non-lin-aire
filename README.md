# Solveur d'Optimisation Non Lineaire

Application web pour resoudre des problemes d'optimisation non lineaire en utilisant GEKKO et Streamlit.

## Description

Cette application permet de definir et resoudre des problemes d'optimisation avec :

- Variables de decision (x1, x2, x3, ...)
- Fonction objective a minimiser ou maximiser
- Contraintes d'egalite (==) et d'inegalite (<=, >=)
- Bornes sur les variables

Le solveur utilise IPOPT via la bibliotheque GEKKO pour trouver la solution optimale.

## Installation

1. Cloner le depot :
```bash
git clone <url-du-repo>
cd Solveur
```

2. Creer et activer un environnement virtuel :
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. Installer les dependances :
```bash
pip install -r requirements.txt
```

## Utilisation

Lancer l'application :
```bash
streamlit run SolveurApp.py
```

L'application s'ouvrira dans votre navigateur par defaut.

### Syntaxe des expressions

- **Variables** : x1, x2, x3, ...
- **Operateurs** : +, -, *, /, **
- **Exemples** :
  - `2*x1**2 + x2`
  - `x1*x2 - 4*x1`
  - `x1**2 + 5*x2`

### Exemples predefinies

L'application inclut plusieurs exemples predefinies accessibles depuis la barre laterale :

- Exemple 1 (cours) : Probleme avec 3 variables et 2 contraintes
- Exemple 2 (simple) : Probleme avec 2 variables
- Exemple 3 (complexe) : Probleme avec 3 variables et 3 contraintes

## Dependances

- streamlit >= 1.28.0
- gekko >= 1.0.6
- numpy >= 1.24.0
- pandas >= 2.0.0

