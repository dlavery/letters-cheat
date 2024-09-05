#!/usr/bin/python3
import psycopg2
import config

def update_db(conn, cur, str, debug=False):
    # do DB updates for wordlist
    r = str.strip().lower()
    if debug:
        print(r)
    cur.execute(
        "INSERT INTO " + conn.info.dbname + ".rawwords (word) " + 
        "VALUES (%s) RETURNING word_id", 
        (r, ))
    conn.commit()

if __name__ == '__main__':
    cfg = config.load_config()
    conn = None
    try:
        # connect to the PostgreSQL server
        with psycopg2.connect(**cfg) as conn:
            conn.set_session(autocommit=False)
            with conn.cursor() as cur:
                # open and process words file
                with open("english-words/words_alpha.txt", mode="r") as file:
                    r = file.readline()
                    ctr = 1
                    while r:
                        r = r.strip()
                        l = len(r)
                        # discard trivial words
                        if l > 3:
                            # add to DB
                            update_db(conn, cur, r, False)
                        r = file.readline()
                        ctr+= 1
                        if ctr // 1000 == ctr / 1000:
                            print(ctr, "words loaded")
                        #if ctr > 10000: # for testing
                        #    break
        print(ctr, "words loaded")
    except (psycopg2.DatabaseError, Exception) as error:
        if conn:
            conn.rollback()
        print(error)
