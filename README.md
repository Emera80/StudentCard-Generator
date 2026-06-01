# 🪪 StudentCard-Generator — Système Automatique de Cartes Étudiantes & Vérification QR

[![Django](https://img.shields.io/badge/Framework-Django%205.x-092E20?style=for-the-badge&logo=django&logoColor=white)](https://docs.djangoproject.com/)
[![Cloudinary](https://img.shields.io/badge/Storage-Cloudinary-3448C5?style=for-the-badge&logo=cloudinary&logoColor=white)](https://cloudinary.com/)
[![Render](https://img.shields.io/badge/Deployment-Render-46E3B7?style=for-the-badge&logo=render&logoColor=black)](https://render.com/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

**StudentCard-Generator** est une application web robuste développée avec Django 5, conçue pour automatiser la création, la gestion et la vérification sécurisée des cartes d'étudiants. Grâce à l'intégration de codes QR dynamiques et d'un stockage cloud asynchrone, le système permet une identification instantanée et fiable des étudiants.

---

## 🚀 Fonctionnalités Clés

- **🎲 Génération Automatisée par Signaux** : Utilisation des signaux `post_save` de Django pour déclencher la création du QR code immédiatement après l'enregistrement d'un étudiant (`Etudiant`) en base de données.
- **🔒 Encodage Sécurisé Base64** : Les données critiques (matricule et identifiant unique) sont chiffrées en Base64 URL-safe, garantissant l'intégrité des informations lors du scan et de la transmission via URL.
- **🔗 Résolution d'URLs Absolues** : Détection automatique de l'environnement (Local vs Production sur Render) via `settings.DOMAIN` pour générer des QR codes scannables universellement.
- **🎨 Design Royal Customisé** : QR codes générés en haute résolution avec une esthétique personnalisée (Bleu Royal `#1e40af` sur fond blanc).
- **☁️ Gestion des Flux Mémoire (Cloud-Ready)** : Optimisation des performances via `BytesIO`. L'image est manipulée en mémoire vive, évitant les écritures disque inutiles avant son transfert direct vers Cloudinary.
- **🔍 Système de Vérification Intégré** : Interface dédiée pour scanner et valider instantanément le statut d'un étudiant en temps réel.

---

## 🛠️ Stack Technique

- **Backend** : Python 3.x, Django 5.x
- **Base de données** : PostgreSQL (Production via Supabase/dj-database-url) / SQLite (Développement)
- **Librairies Graphiques** : `qrcode`, `Pillow`
- **Gestion des Fichiers** : `Cloudinary` (Images), `WhiteNoise` (Fichiers statiques)
- **Déploiement** : Render (Infrastructure managée)
- **Environnement** : `python-dotenv` pour la gestion des variables secrètes

---

## 📂 Architecture Logicielle

### Modèle de Données (Core)
Le système s'appuie sur une structure hiérarchique garantissant l'intégrité référentielle :
- `Etudiant` : Entité centrale (Matricule, Nom, Postnom, Prénom, Sexe, Photo/QR).
- `Promotion` : Niveau d'étude.
- `Faculte` : Rattachement académique.
- `Section` : Organisation structurelle supérieure.

### Logique des Signaux (`etudiants/signals.py`)
Le cœur de l'automatisation réside dans l'interception du cycle de vie des modèles :

```python
@receiver(post_save, sender=Etudiant)
def generate_qr_code(sender, instance, created, **kwargs):
    if created or not instance.qr_code:
        # 1. Préparation des données sécurisées
        qr_data = f"ETUDIANT:{instance.matricule}:{instance.qr_code_data}"
        encoded_qr_data = base64.urlsafe_b64encode(qr_data.encode()).decode()
        
        # 2. Construction de l'URL de vérification
        absolute_url = f"{settings.DOMAIN}{reverse('verify_qr', args=[encoded_qr_data])}"
        
        # 3. Génération binaire et repositionnement du curseur (buffer.seek(0))
        # 4. Persistance sur Cloudinary via le stockage par défaut de Django
```

---

## ⚙️ Installation et Configuration

### 1. Clonage et Dépendances
```bash
git clone https://github.com/Emera80/StudentCard-Generator.git
cd StudentCard-Generator
pip install -r requirements.txt
```

### 2. Variables d'Environnement
Créez un fichier `.env` à la racine :
```env
SECRET_KEY=votre_cle_secrete
DEBUG=True
CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
RENDER_EXTERNAL_URL=http://127.0.0.1:8000
```

### 3. Initialisation de la Base de Données
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## 📈 Défis Résolus & Optimisations

Le principal défi technique a été la transition vers un stockage cloud strict (sans système de fichiers local persistant). L'erreur courante de "fichier vide" lors de l'upload vers Cloudinary a été résolue par une manipulation précise du pointeur binaire. 

En utilisant `buffer.seek(0)` après la sauvegarde de l'image dans le flux `BytesIO`, nous avons forcé le moteur de stockage de Django à lire les données depuis le début du tampon, permettant une transmission fluide et sans erreur vers les serveurs de Cloudinary.

---

## 👨‍💻 Auteur

**Emera** — Étudiant en 2e Licence Informatique
- Portefolio : [Mon Portefolio](https://lien_portefolio)
- GitHub : [@Emera80](https://github.com/Emera80)
---

*Projet axé sur la maîtrise des processus d'automatisation (Signaux Django), de la manipulation de flux de données et de la sécurisation des endpoints applicatifs.*
