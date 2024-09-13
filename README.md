# letters-cheat
Cheat at the Countdown letters game

Impress your friends by cheating at Countdown...

(Needs PostgreSQL to be downloaded and installed, https://www.postgresql.org/)

Simply create a PostgreSQL database using the db-init.sql file in the db-migrations folder, then clone the git repo at https://github.com/InnovativeInventor/english-words.git to get a list of English words. Change the database.ini file to match your DB parameters and then load the english wordset into the DB using the loadwords python script. Run findwords.py to enter your 9 letters and get back a list of possible solutions.

Bingo, you're an octo-champ!

And NOW...

Cheat at Wordle!

Add the new table to the wordlist database using the db-rawwords.sql file in the db-migrations folder then run loadrawwords.py to populate the table from the english-words list. Run findwordle.py where you will be asked to enter your attempts and the responses to them. Type "exit" or "quit" here to exit the program, type "done" at the attempt prompt once you have entered your attempts to receive solution hints. Reponses should be coded as:
y - yes, correct letter in the correct place
n - no, incorrect letter
o - other, correct letter in the incorrect place

e.g. if the word is "beast" and your attempt is "baker" then the response would be "yonon" (green, yellow, grey, yellow, grey on most apps/sites).

You can also use this to suggest solutions when you're fairly sure you know the target word has a specific prefix or suffix. For example, if you're pretty certain a 9 letter wordle starts with "inter", you can enter "interxxxx" as your attempt and use "yyyyy...." as the response ("." is a neutral character and so doesn't affect the algorithm). You'll then receive a hint list that contains: interacts, interbred, etc.