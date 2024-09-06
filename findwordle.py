#!/usr/bin/python3
import psycopg2
import config
import sys

def do_wordle(cfg:dict, attempts:str, debug:bool=False) -> list[tuple]:
        conn = None
        present = []
        not_present = []
        pattn = ['^']
        for i in range(len(attempts[0][1])):
            pattn.append('.') 
        qry = "SELECT rawwords.word from " + cfg['dbname'] + ".rawwords WHERE "
        for attempt, res in attempts:
            for i in range(len(res)):
                if res[i] == 'o':
                    if attempt[i] not in present:
                        present.append(attempt[i])
                    try:
                        not_present.remove(attempt[i])
                    except ValueError:
                        pass
                    if pattn[i+1] == '.':
                        pattn[i+1] = [attempt[i]]
                    elif type(pattn[i+1]) == list:
                        pattn[i+1].append(attempt[i])
                elif res[i] == 'n':
                    if attempt[i] not in not_present \
                    and attempt[i] not in present \
                    and attempt[i] not in pattn:
                        not_present.append(attempt[i])
                    if pattn[i+1] == '.':
                        pattn[i+1] = [attempt[i]]
                    elif type(pattn[i+1]) == list:
                        pattn[i+1].append(attempt[i])
                elif res[i] == 'y':
                    try:
                        present.remove(attempt[i])
                    except ValueError:
                        pass
                    try:
                        not_present.remove(attempt[i])
                    except ValueError:
                        pass
                    pattn[i+1] = attempt[i]
        str_pattn = ''
        for p in pattn:
            if type(p) == str:
                str_pattn += p
            elif type(p) == list:
                tmp = ''.join(p)
                str_pattn = str_pattn + '[^' + tmp + ']'
        if str_pattn[-1] == '.' or str_pattn[-1] == 's':    
            # shorten matching pattern to accomodate plurals
            str_pattn = str_pattn[:-1]
        qry = qry + "word ~ '" + str_pattn + "' "
        for p in present:
            qry = qry + "AND word ~ '" + p + "' "
        for n in not_present:
            qry = qry + "AND word !~ '" + n + "' "
        # include singular words in search where plural may be the answer
        qry = qry + "AND length(word)>=" + str(len(attempts[0][0])-1) + " AND length(word)<=" + str(len(attempts[0][0])) + " "
        qry = qry + "ORDER BY rawwords.word ASC LIMIT 20"
        if debug:
            print(qry)
        words = []
        try:
            # connect to the PostgreSQL server
            with psycopg2.connect(**cfg) as conn:
                with conn.cursor() as cur:
                    cur.execute(qry)
                    rows = cur.fetchall()
                    for r in rows:
                        if len(r[0]) < len(attempts[0][0]):
                            words.append(r[0]+'(s)')
                        else:
                            words.append(r[0])
                    return(words)
        except (psycopg2.DatabaseError, Exception) as error:
            return (error)
    
if __name__ == '__main__':
    debug = False
    if '-d' in sys.argv:
        debug = True
    while True:
        attempts = []
        while True:
            attempt = input("Enter your attempt: ").strip().lower()
            if attempt == 'exit' or attempt == 'quit':
                exit(0)
            if attempt == 'done':
                break
            if attempt:
                if attempts and len(attempt) != len(attempts[0][0]):
                    print("Please try again")
                else:
                    while True:
                        res = input("Enter the result: ").strip().lower()
                        if len(res) != len(attempt):
                            print("Please try again")
                        else:
                            attempts.append((attempt, res))
                            break
        cfg = config.load_config()
        words = do_wordle(cfg, attempts, debug)
        print("-----------------")
        print("HINTS:")
        for w in words:
            print(w)
        print("-----------------")
        cont = input("Again (N)? ").strip().lower()
        if cont != 'y':
            break
