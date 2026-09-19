# backend_student — PostgreSQL local (Docker)

Dossier dédié à la base **StudentCard-Generator**, pour ne pas le confondre avec `STEG-PLATEFORME/backend` (MySQL).

| Élément | Nom |
|--------|-----|
| Projet Compose | `backend_student` |
| Conteneur | `backend_student_postgres` |
| Volume | `backend_student_postgres_data` |
| Port sur ta machine | **5434** → 5432 dans le conteneur |

## Docker Desktop

1. Ouvrir le **Compose file viewer** sur ce dossier :  
   `StudentCard-Generator/backend_student`
2. Démarrer la stack (ou en terminal, depuis ce dossier) :

```powershell
docker compose up -d
```

3. Arrêter quand tu as fini :

```powershell
docker compose stop
```

Copier `../.env.example` vers `../.env` à la racine du dépôt et ajuster `SECRET_KEY` / `CLOUDINARY_URL`.
