#!/usr/bin/python3
import psycopg2
import config
import sys

def make_sql(attempts:list, debug:bool=False, trunc:int=0) -> str:
        present = []
        not_present = []
        pattn = ['^']
        new_attempts = []
        orig_len = len(attempts[0][0])
        if trunc > 0:
            trunc = trunc * -1
            for a, r in attempts:
                new_attempts.append((a[:trunc], r[:trunc]))
            attempts = new_attempts
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
        #if str_pattn[-1] == '.' or str_pattn[-1] == 's':    
        #    # shorten matching pattern to accomodate plurals
        #    str_pattn = str_pattn[:-1]
        qry = qry + "word ~ '" + str_pattn + "' "
        for p in present:
            qry = qry + "AND word ~ '" + p + "' "
        for n in not_present:
            qry = qry + "AND word !~ '" + n + "' "
        # include singular words in search where plural may be the answer
        #qry = qry + "AND length(word)>=" + str(len(attempts[0][0])-1) + " AND length(word)<=" + str(len(attempts[0][0])) + " "
        qry = qry + "AND length(word)>=" + str(len(attempts[0][0])) + " AND length(word)<=" + str(orig_len) + " "
        qry = qry + "ORDER BY rawwords.word ASC LIMIT 25"
        if debug:
            print(qry)
        return qry

def do_wordle(cfg:dict, attempts:list, debug:bool=False) -> list[tuple]:
        conn = None
        words = []
        try:
            # connect to the PostgreSQL server
            with psycopg2.connect(**cfg) as conn:
                with conn.cursor() as cur:
                    trunc = 0
                    while True:
                        qry = make_sql(attempts, debug, trunc)
                        cur.execute(qry)
                        rows = cur.fetchall()
                        for r in rows:
                            #if len(r[0]) < len(attempts[0][0]):
                            #    words.append(r[0]+'(s)')
                            #else:
                            #    words.append(r[0])
                            words.append(r[0])
                        trunc += 1
                        if len(words) > 0 or trunc > 4:
                            break
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
                elif len(attempt) < 5:
                    print("Too short - please try again")
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
        if type(words) == list:
            for w in words:
                print(w)
            print("-----------------")
            cont = input("Again (N)? ").strip().lower()
        else:
            print(words)
            cont='n'
        if cont != 'y':
            break
'''
TESTS
=====
1.
Inputs:
Enter your attempt: juggernaut
Enter the result: nynnonnnnn
Enter your attempt: bumblebees
Enter the result: nyonyynnny
Enter your attempt: done

Expected:
cuddlesome
huddledom
muddledom
muddlesome
muffledly
musclelike
muzzlewood
puzzledom

2.
Enter your attempt: vengeance
Enter the result: noonnonyn
Enter your attempt: ambulance
Enter the result: ononnnoyo
Enter your attempt: breakneck
Enter the result: yooononyn
Enter your attempt: done

Expected:
baronetcy

3.
Enter your attempt: juggernaut
Enter the result: nonnnnnonn
Enter your attempt: acquiesced
Enter the result: ynooonnnnn
Enter your attempt: done

Expected:
aquaphobia

4.
Enter your attempt: aquashapes 
Enter the result: yyyyonnnon
Enter your attempt: done

Expected:
aquacades
aquatones

5.
Enter your attempt: stationer
Enter the result: onnnoooon
Enter your attempt: gestation
Enter the result: noonnnooo
Enter your attempt: splendour
Enter the result: onooonoon
Enter your attempt: unisexual
Enter the result: oyooonnno
Enter your attempt: inclusive
Enter the result: oynooonoo
Enter your attempt: done

Expected:
enviously

6.
Enter your attempt: juggernaut
Enter the result: nynnnnnonn
Enter your attempt: automation
Enter the result: oynnnnnonn
Enter your attempt: fundaments
Enter the result: nynnonnnny
Enter your attempt: supplicant
Enter the result: oynnyooonn
Enter your attempt: done

Expected:
quillbacks
'''