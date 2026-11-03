# API SoftDesk

## Synthèse

SoftDesk est une API REST de gestion de projets, de contributeurs, de problèmes et de commentaires.
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

L’application a besoin d’une clé secrète Django dans un fichier `.env` à la racine du projet. Générez-en une :

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

L’API est alors disponible à `http://127.0.0.1:8000/api/`. Pour créer un compte administrateur local, lancez `poetry run python manage.py createsuperuser`.

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
