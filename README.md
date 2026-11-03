# API SoftDesk

## Synthèse

SoftDesk est une API REST de gestion de tickets support avec la notion de projet, de contributeurs, de problèmes et de commentaires.
Elle utilise Django REST Framework et l’authentification JWT.
Les projets sont accessibles à leurs contributeurs, et certaines modifications sont réservées à leur auteur.

## Installation en local

### Prérequis

- Python 3.12 ou une version supérieure
- Poetry
- Git

### Installer et démarrer le projet

```bash
git clone https://github.com/Nels-J/P10_Cr-ez-une-API-s-curis-e-RESTful-en-utilisant-Django-REST.git
cd P10_Cr-ez-une-API-s-curis-e-RESTful-en-utilisant-Django-REST
poetry install
```

L’application a besoin d’une clé secrète Django dans un fichier `.env` à la racine du projet.
Générez-en une avec la commande suivante :

```bash
poetry run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Créez ensuite `.env` et ajoutez la clé obtenue :

```env
DJANGO_SECRET_KEY=votre-cle-secrete-generee
```

Initialisez la base SQLite locale et démarrez le serveur :

```bash
poetry run python manage.py migrate
poetry run python manage.py runserver
```

L’API est alors disponible à `http://127.0.0.1:8000/api/`.

Pour créer un compte administrateur local, lancez :
```bash
poetry run python manage.py createsuperuser
```

## Tester l’API
Les requêtes peuvent être envoyées avec Postman, Insomnia ou un outil équivalent. Pour les routes privées, commencez par créer un compte avec `POST /api/users/`, puis obtenez un jeton avec `POST /api/auth/jwt/create/` en envoyant `username` et `password`. Dans l’outil, utilisez le jeton `access` reçu comme jeton Bearer.

Dans le tableau, « public » signifie qu’aucun jeton d’accès n’est nécessaire. Les routes privées demandent un jeton JWT valide ; les droits indiqués précisent les restrictions supplémentaires.

| Méthode | Endpoint | Accès |
|---|---|---|
| POST | `/api/auth/jwt/create/` | Public — obtention des jetons |
| POST | `/api/auth/jwt/refresh/` | Public — nécessite un jeton `refresh` dans le corps |
| POST | `/api/auth/jwt/verify/` | Public — nécessite un jeton dans le corps |
| POST | `/api/users/` | Public — inscription |
| GET | `/api/users/` | Privé — utilisateur connecté |
| GET, PATCH | `/api/users/me/` | Privé — utilisateur connecté, accès à son propre profil |
| GET, POST | `/api/projects/` | Privé — utilisateur connecté |
| GET | `/api/projects/{project_id}/` | Privé — contributeur du projet |
| PATCH, DELETE | `/api/projects/{project_id}/` | Privé — auteur du projet |
| GET | `/api/projects/{project_id}/contributors/` | Privé — contributeur du projet |
| POST | `/api/projects/{project_id}/contributors/` | Privé — utilisateur connecté |
| GET, POST | `/api/projects/{project_id}/issues/` | Privé — contributeur du projet |
| GET | `/api/projects/{project_id}/issues/{issue_id}/` | Privé — contributeur du projet |
| PATCH, DELETE | `/api/projects/{project_id}/issues/{issue_id}/` | Privé — auteur du problème |
| GET, POST | `/api/projects/{project_id}/issues/{issue_id}/comments/` | Privé — contributeur du projet |
| GET | `/api/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/` | Privé — contributeur du projet |
| PATCH, DELETE | `/api/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/` | Privé — auteur du commentaire |


## Collection Postman
Une collection Postman est disponible dans le repository pour tester les endpoints de l'API.
Emplacement : postman/collections/API_SOFTDESK.postman_collection.json

#### Import et configuration
- Ouvrir Postman et cliquer sur Import.
- Sélectionner le fichier JSON de la collection.
- Définir le AuthType à Bearer Token dans l'onglet Authorization pour les requêtes privées.
- Configurer les variables d'environnement :

|Variable|Description|
|---|---|
|base_url|URL de base de l'API (ex. http://127.0.0.1:8000 )|
|access_token|Token JWT pour l'authentification|
|refresh_token|Token JWT pour le rafraîchissement|
|username|Nom d'utilisateur pour l'authentification|
|password|Mot de passe pour l'authentification|
|project_id|ID du projet pour les requêtes spécifiques|
|issue_id|ID du problème pour les requêtes spécifiques|
|comment_id|ID du commentaire pour les requêtes spécifiques|
 
> Certaines variables seront automatiquement mises à jour après l'exécution des requêtes d'authentification et de création de ressources.
> Des scripts sont présents dans le but de faciliter les tests, néanmoins, il est recommandé de vérifier les valeurs des variables avant d'exécuter les requêtes.
> Il est possible de modifier ponctuellement les valeurs des variables pour tester différents scénarios.

#### Mise à jour
Toute modification de la collection doit être exportée au format Postman Collection v2.1 et versionnée dans le repository GitHub.
Sécurité : ne jamais versionner de tokens, mots de passe ou autres informations sensibles.