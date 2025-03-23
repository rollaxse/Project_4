FROM postgres
ENV POSTGRES_PASSWORD=docker
ENV POSTGRES_DB=WORLD 
COPY world.sql /docker-entrypoint-initdb.d/
