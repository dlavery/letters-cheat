#!/usr/bin/python3
import psycopg2
import config
import wordutils
import time

def do_words(cfg:dict, letters:str, max_words:int) -> list[tuple]:
        conn = None
        words = []
        sample_size = len(letters)
        try:
            # connect to the PostgreSQL server
            with psycopg2.connect(**cfg) as conn:
                with conn.cursor() as cur:
                    while sample_size > 3 and len(words) < max_words:
                        combinations = wordutils.get_combinations(letters, sample_size)
                        for comb in combinations:
                            cur.execute(
                                "SELECT tokens.token, words.word from " + conn.info.dbname + ".tokens " +
                                "LEFT JOIN " + conn.info.dbname + ".tokens_words ON tokens_words.tokens_id=tokens.token_id " +
                                "LEFT JOIN " + conn.info.dbname + ".words ON words.word_id=tokens_words.words_id " +
                                "WHERE tokens.token=%s",
                                (comb,))
                            rows = cur.fetchall()
                            for r in rows:
                                if len(words) < max_words: 
                                    lr1 = len(r[1])
                                    if (lr1, r[1]) not in words:
                                        words.append((lr1, r[1]))
                                else:
                                    break
                            if len(words) >= max_words:
                                break
                        sample_size-= 1
                    return(words)
        except (psycopg2.DatabaseError, Exception) as error:
            return (0, error)
    
if __name__ == '__main__':
    while True:
        letters = input("Enter your letters: ").strip().lower()
        if letters == 'exit' or letters == 'quit':
            exit(0)
        if len(letters) != 9:
            continue
        cfg = config.load_config()
        starttime = time.time()
        words = do_words(cfg, letters, 10)
        endtime = time.time()
        print("-----------")
        for w in words:
            print(w[0], w[1])
        print("Execution:", int(endtime - starttime), "seconds")
        print("-----------")