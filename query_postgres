import sqlalchemy as sa
from sqlalchemy_utils import database_exists, create_database
import json, os

# Reading credentials

db_user = "postgres"
db_pass = "qwertyu"


uri = f'postgresql://{db_user}:{db_pass}@localhost:5432/noticias'

engine = sa.create_engine(uri, echo=True)

if not database_exists(engine.url):
    print("Creando la base de datos")
    create_database(engine.url)

with engine.connect().execution_options(autocommit=True) as con:
    result = con.execute(sa.sql.text("""
            CREATE TABLE IF NOT EXISTS news (
                n INTEGER,
                id integer PRIMARY KEY, 
                title text,
                publication text,
                author text,
                date text,
                year text, 
                month text, 
                url text, 
                content text
            );
            alter table news add column content_ts tsvector;
            create index idx_content_ts on news using gin (content_ts);
    """))
    print(result)
