# letters-cheat
Cheat at the Countdown letter game

Impress your friends by cheating at Countdown...

Simply create a PostgreSQL database using the db-init.sql file in the db-migrations folder, then clone the git repo at https://github.com/InnovativeInventor/english-words.git to get a list of English words. Change the database.ini file to match your DB parameters and then load the english wordset into the DB using the loadwords python script. Run findwords.py to enter your 9 letters and get back a list of possible solutions.

Bingo, you're an octo-champ!

And NOW...

Cheat at Wordle!

Add the new table to the wordlist database using the db-rawwords.sql file in the db-migrations folder then run loadrawwords.py to populate the table from the english-words list. Run findwordle.py where you will be asked to enter your attempts and the responses to them. Type "exit" or "quit" here to exit the program, type "done" once you have enterted your attempts to receive solution hints. Reponses should be coded as:
y - correct letter in the correct place
o - correct letter in the incorrect place
n - incorrect letter

e.g. if the word is "beast" and your attempt is "baker" then the response would be "yonon".