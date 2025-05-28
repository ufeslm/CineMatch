# Système de Recommandation de Films

## Fonctionnalités Principales

### 1. Authentification Utilisateur
- **Inscription** : Création de compte avec nom d'utilisateur et email
- **Connexion** : Accès sécurisé à l'application
- **Gestion de Session** : Maintien de la connexion utilisateur

### 2. Recherche de Films
- **Barre de Recherche** : Accessible depuis n'importe quelle page
- **Recherche en Temps Réel** : Utilisation de l'API TMDB
- **Affichage des Résultats** : Posters, titres et détails des films

### 3. Système de Recommandations
- **Recommandations Personnalisées** : Basées sur les films favoris
- **Filtres Intelligents** :
  - Note minimale (6.0/10)
  - Année de sortie (2018 et plus récent)
  - Limite de 20 films recommandés
- **Élimination des Doublons** : Pas de répétition dans les suggestions

### 4. Gestion des Listes
- **Films Favoris** :
  - Ajout/Suppression de films
  - Influence sur les recommandations
  - Stockage persistant
- **À Regarder Plus Tard** :
  - Liste séparée des favoris
  - Suivi des films à voir
  - Accessible depuis la page des recommandations

### 5. Notifications
- **Notifications par Email** :
  - Alertes pour les nouvelles recommandations
  - Configuration personnalisable
  - Système découplé utilisant le pattern Observer

## Technologies Utilisées

### Backend
- Python 3.x
- Flask (Framework Web)
- SQLAlchemy (ORM)
- Flask-Login (Authentification)
- Flask-Mail (Notifications Email)
- Requests (Appels API)

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- Font Awesome (Icônes)

### Base de Données
- SQLite

### API Externe
- The Movie Database (TMDB) API

## Comment Utiliser l'Application

1. **Première Utilisation** :
   - Créer un compte
   - Se connecter avec ses identifiants

2. **Recherche de Films** :
   - Utiliser la barre de recherche
   - Consulter les détails des films
   - Ajouter des films aux favoris

3. **Obtenir des Recommandations** :
   - Ajouter des films aux favoris
   - Visiter la page des recommandations
   - Découvrir des films similaires
   - Ajouter des films à la liste "À regarder plus tard"

4. **Gérer ses Listes** :
   - Consulter ses films favoris
   - Gérer sa liste "À regarder plus tard"
   - Supprimer des films des listes

## Fonctionnalités Avancées

### Patterns de Conception Implémentés

1. **Pattern Strategy** :
   - Algorithmes de recommandation interchangeables
   - Filtrage collaboratif
   - Filtrage basé sur le contenu
   - Recommandation hybride

2. **Pattern Observer** :
   - Système de notification découplé
   - Notifications par email
   - Mises à jour des recommandations

3. **Pattern Decorator** :
   - Filtres dynamiques pour les recommandations
   - Filtrage par note
   - Filtrage par année
   - Filtrage par genre

4. **Pattern Command** :
   - Actions sur les films encapsulées
   - Ajout aux favoris
   - Suppression des favoris
   - Gestion de la liste "À regarder plus tard"

5. **Pattern State** :
   - Gestion des états du processus de recommandation
   - État initial
   - État de traitement
   - État prêt

## Configuration Requise

1. **Installation des Dépendances** :
   ```bash
   pip install flask flask-sqlalchemy flask-login flask-mail requests python-dotenv
   ```

2. **Configuration** :
   - Clé API TMDB
   - Configuration email (Gmail)
   - Variables d'environnement

3. **Base de Données** :
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

## Améliorations Futures

1. Préférences utilisateur pour les filtres
2. Fonctionnalités sociales (partage de recommandations)
3. Système de critiques et notes
4. Algorithmes de recommandation plus sophistiqués
5. Intégration avec les services de streaming
6. Personnalisation du profil utilisateur
7. Préférences de genres
8. Historique des recommandations 