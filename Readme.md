# ZillowPrediction : Application de Prédiction des Prix Immobiliers

Cette application Flask permet d'estimer la valeur d'une propriété en utilisant un modèle de prédiction basé sur des données immobilières. Les utilisateurs peuvent entrer diverses caractéristiques de la propriété, et l'application renvoie une estimation du prix.
La dataset, le model et le fichier jupyter sont contenu dans le dossier model.

## Fonctionnalités

- Estimation du prix d'une propriété basée sur les caractéristiques fournies :
  - Surface habitable
  - Année de construction
  - Nombre de chambres
  - Nombre de salles de bain
  - Type de propriété
  - Ville, comté et adresse
- Interface utilisateur conviviale avec des formulaires simples
- Traitement des requêtes en temps réel grâce à AJAX
- Affichage des résultats de manière claire et lisible

## Technologies Utilisées

- Python
- Flask
- HTML/CSS
- JavaScript (avec jQuery)
- Bootstrap pour le design
- Modèle de prédiction (Régression linéaire)

## Prérequis

Avant de commencer, assurez-vous d'avoir installé Python 3 et pip (le gestionnaire de packages Python).

## Installation

1. **Clonez le dépôt :**

   ```bash
   git clone https://github.com/NAJPRO/NAJ_PredictionHouse.git
   cd NAJ_PredictionHouse

2. **Créez un nouvel environnement virtuel :**

   ```bash
   python -m venv venv

3. **Activez l'environnement virtuel :**
   - Sur Windows :
     ```bash
     venv\Scripts\activate
     ```
   - Sur macOS/Linux :
     ```bash
     source venv/bin/activate
     ```

4. **Installez les dépendances :**
   ```bash
   pip install -r requirements.txt


# Utilisation

1.  **Lancez l'application :**
    ```bash
    flask run

2. **Accédez à l'application :**
    Ouvrez votre navigateur et allez à http://127.0.0.1:5000

3. **Remplissez le formulaire :**
   - Entrez les détails de la propriété dans le formulaire.
   - Cliquez sur le bouton "Estimer" pour obtenir une estimation du prix.

4. **Visualisez les résultats :**
    L'estimation du prix s'affichera sous le formulaire après quelques instants.
