from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed = pwd_context.hash("admin123")
print(hashed)


#PASOS PARA LEVANTAR BASE DE DATOS DE PRUEBAS

#1. Copia backup_horarios.sql al nuevo entorno.

#2. Levanta tus contenedores normalmente (docker compose up -d).

#3. Carga el backup en la base de datos ya levantada:

##4. docker cp backup_horarios.sql backend-horarios-db-1:/backup_horarios.sql

##5. docker exec -i backend-horarios-db-1 psql -U postgres -d horarios < /backup_horarios.sql
