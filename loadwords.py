#!/usr/bin/python3
import psycopg2
import config

def update_db(conn, cur, str, debug=False):
    # do DB updates for wordlist
    r = str.strip().lower()
    if debug:
        print(r)
    cur.execute(
        "INSERT INTO " + conn.info.dbname + ".words (word) " + 
        "VALUES (%s) RETURNING word_id", 
        (r, ))
    ret = cur.fetchone()
    word_id = ret[0]
    token = ''.join(sorted(r))
    if debug:
        print(token)
    cur.execute(
        "SELECT token_id FROM " + conn.info.dbname + ".tokens " + 
        "WHERE token = %s", 
        (token,))
    ret = cur.fetchone()
    if ret:
        token_id = ret[0]
    else:
        cur.execute(
            "INSERT INTO " + conn.info.dbname + ".tokens (token) " + 
            "VALUES (%s) RETURNING token_id", 
            (token,))
        ret = cur.fetchone()
        token_id = ret[0]
        if debug:
            print('tokens inserted')
    cur.execute(
        "INSERT INTO " + conn.info.dbname + ".tokens_words (tokens_id, words_id) " + 
        "VALUES (%s, %s)",
        (token_id, word_id))
    if debug:
        print('tokens_words inserted')
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
                        # discard trivial words and those > 9 characters
                        if l > 3 and l < 10:
                            # add to DB
                            debug = False
                            update_db(conn, cur, r)
                        r = file.readline()
                        #ctr+= 1
                        #if ctr > 10000: # for testing
                        #    break
    except (psycopg2.DatabaseError, Exception) as error:
        if conn:
            conn.rollback()
        print(error)
