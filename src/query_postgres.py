import sqlalchemy as sa
from sqlalchemy_utils import database_exists, create_database
import time
import json, os
import pandas as pd
import csv
# Reading credentials

db_user = "postgres" ## poner el user del docker
db_pass = "mysecretpassword"  ## poner el password del docker
dirPath = "/data/arxiv"  ## poner el directorio donde estan los abstracts

## colocar (id,abstract) en un csv
dirCSV ='/data/papers_arxiv.csv'



uri = f'postgresql://{db_user}:{db_pass}@db:5432/noticias'

engine = sa.create_engine(uri)

if not database_exists(engine.url):
    create_database(engine.url)

with engine.connect().execution_options(autocommit=True) as connection:
    data = connection.execute(sa.sql.text("""
            CREATE TABLE IF NOT EXISTS papers (
                id text PRIMARY KEY,
                abstract text
            );
            alter table papers add column if not exists content_ts tsvector;
            create index if not exists idx_content_ts on papers using gin (content_ts);
    """))

    data = connection.execute(sa.sql.text("""
            TRUNCATE TABLE papers
    """))

    data = connection.execute(sa.sql.text(f"""
            COPY papers(id,abstract) 
            FROM '{dirCSV}'
            DELIMITER ','
            CSV HEADER;
    """))

    data = connection.execute(sa.sql.text("""
            update papers
            set content_ts = x.content_ts
            from (
            select Id, 
                    setweight(to_tsvector('english', abstract), 'A')
                    as content_ts
            from papers
            ) as x
            where x.Id = papers.Id;
    """))



def TopK_answer(text, k):
    with engine.connect().execution_options(autocommit=True) as connection:
        ans_all = []
        start = time.time()
        data = connection.execute(sa.sql.text(f""" 
            select abstract,ts_rank_cd(content_ts, query_ts) as score
            from papers, to_tsquery('english', '{text}') query_ts
            where query_ts @@ content_ts
            order by score desc 
            limit {k};
        """))
        end = time.time()
        total_time = round(end - start, 8)       
        for row in data:
            dict1 = {}
            dict1['abstract'] = row['abstract']
            dict1['score'] = row['score']
            ans_all.append(dict1)

        response = { "data": ans_all, "time": total_time } 

    return response

