-- Database: wordlist => ADD ALL OF THE WORDS
    
-- Table: wordlist.rawwords

DROP TABLE IF EXISTS wordlist.rawwords;

CREATE TABLE IF NOT EXISTS wordlist.rawwords
(
    word_id integer NOT NULL DEFAULT nextval('wordlist.words_id_seq'::regclass),
    word character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT rawword_id PRIMARY KEY (word_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS wordlist.rawwords
    OWNER to postgres;
-- Index: word

-- DROP INDEX IF EXISTS wordlist.rawword;

CREATE INDEX IF NOT EXISTS rawword
    ON wordlist.rawwords USING btree
    (word COLLATE pg_catalog."default" ASC NULLS LAST)
    WITH (deduplicate_items=True)
    TABLESPACE pg_default;
