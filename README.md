# Planning Poker - Projet Agile (M1 Informatique)

Ce projet a été réalisé en binôme dans le cadre du cours **Conception Agile de Projets Informatiques**.

L'objectif était de développer une application de bureau pour faciliter les sessions de Planning Poker. Elle permet de remplacer les jeux de cartes physiques et gère automatiquement les règles de consensus (moyenne, médiane, etc.) lors des votes.

## Fonctionnalités principales

L'application permet de gérer une session complète :

- **Configuration :** Ajout des joueurs et import des tâches (Backlog) depuis un fichier JSON ou manuellement.
- **Déroulement :** Les joueurs votent chacun leur tour (les cartes sont cachées).
- **Règles de gestion :**
  - Au premier tour, il faut l'unanimité.
  - Si le vote n'est pas unanime, on applique une règle choisie au lancement (Moyenne, Médiane, Majorité...).
- **Sauvegarde :** Possibilité de mettre en pause et sauvegarder la partie (vote "Café") pour la reprendre plus tard.

## Choix techniques

Le projet est codé en **Python 3.10+**.
Nous avons respecté une architecture **MVC (Modèle-Vue-Contrôleur)** pour séparer la logique métier de l'interface.
L'interface graphique utilise la librairie **CustomTkinter** pour un rendu plus moderne que le Tkinter de base.

## Liens utiles

- Releases (téléchargement du `.exe`) : <https://github.com/LeoAugustinAmy/AMY_LOREL_PlaningPoker/releases>
- Documentation (GitHub Pages) : <https://leoaugustinamy.github.io/AMY_LOREL_PlaningPoker/index.html>

## Téléchargement et utilisation sans cloner

Vous pouvez utiliser l’application sans installer Python ni cloner le dépôt :

- **Téléchargement de l’exécutable Windows (.exe)**  
  Rendez-vous sur la page **Releases** du dépôt GitHub et téléchargez `PlanningPoker.exe` de la dernière version (ex: v2.x).

- **Lancement**  
  Double-cliquez sur `PlanningPoker.exe`. Les ressources (cartes SVG) sont intégrées via la release; aucune configuration supplémentaire n’est requise.

- **Compatibilité**  
  Windows 10+ recommandé. Aucune dépendance Python nécessaire.

## Installation et lancement (mode développement)

Il faut avoir Python et `pip` installés.

1.  **Récupérer le projet :**

    ```bash
    git clone https://github.com/LeoAugustinAmy/AMY_LOREL_PlaningPoker.git
    ```

    ```bash
    cd AMY_LOREL_PlaningPoker.git
    ```

2.  **Installer les dépendances :**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Lancer l'application :**
    ```bash
    python main.py
    ```

## Tests et qualité

Nous avons mis en place des tests unitaires pour valider les calculs (moyennes, règles de vote) et la gestion du backlog.

Pour les lancer :

```bash
python -m unittest tests.py
```

Note : Une CI (GitHub Actions) est configurée pour lancer ces tests automatiquement à chaque push sur les branches principales.

## Utilisation

1.  **Menu Principal** : Cliquez sur `Nouvelle Partie` pour configurer une session ou `Charger Partie` pour reprendre un fichier `.json`.
2.  **Setup** :
    - Ajoutez les pseudos des joueurs.
    - Remplissez le Backlog (ou importez un JSON de tâches).
    - Choisissez la règle de validation (ex: Moyenne).
3.  **Phase de Jeu** :
    - L'application appelle chaque joueur tour à tour.
    - Le joueur sélectionne sa carte (elle reste face cachée).
    - Une fois tous les votes enregistrés, les cartes se retournent.
    - **Résolution** : En cas de désaccord au Tour 1, un débat est lancé. Sinon, la règle choisie s'applique.

## Architecture du projet

Le code est organisé selon le pattern MVC :

- **controllers/** → Logique de contrôle (GameController, SetupController…)
- **models/** → Logique métier (GameSession, Player, Backlog, GameRules)
- **views/** → Interface graphique (CustomTkinter)
- **src/img/** → Ressources graphiques (cartes SVG)
- **.github/workflows/** → Configuration pour l'intégration continue.
