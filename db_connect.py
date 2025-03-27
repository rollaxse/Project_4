import psycopg2

def connection_db():
    return psycopg2.connect(
        dbname="password_vault",
        user="rollaxse",
        password="Houseplant617",
        host="localhost",  # <- important: use host, not socket
        port="5432"
    )

