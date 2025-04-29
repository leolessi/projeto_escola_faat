FROM postgres:14


ENV POSTGRES_DB=escola
ENV POSTGRES_USER=leonardo
ENV POSTGRES_PASSWORD=leonardo

COPY escola.sql /docker-entrypoint-initdb.d/

EXPOSE 5432