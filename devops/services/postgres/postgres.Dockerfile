FROM postgres:16.3-alpine
COPY ./devops/services/postgres/db-build.sql /docker-entrypoint-initdb.d/
