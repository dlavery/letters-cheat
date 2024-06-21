#!/usr/bin/python3
import psycopg2
from config import load_config

def connect(cfg):
    """ Connect to a PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**cfg) as conn:
            print('Connected to the PostgreSQL server, database', conn.info.dbname)
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


if __name__ == '__main__':
    cfg = load_config()
    connect(cfg)