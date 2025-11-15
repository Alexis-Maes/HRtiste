Création de la db postgres

```bash
psql postgres
```

puis
```bash
CREATE DATABASE profile_manager;
CREATE USER admin WITH PASSWORD 'admin';
GRANT ALL PRIVILEGES ON DATABASE profile_manager TO admin;
\q
```





# Modification de la db
Pour modifier les modèles de la db,  toujours appliquer les opérations: 

```bash
alembic revision --autogenerate -m "description_de_la_migration"
```
puis 
```bash
alembic upgrade head
```