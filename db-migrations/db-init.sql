-- Database: wordlist

-- DROP DATABASE IF EXISTS wordlist;

CREATE DATABASE wordlist
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

-- SCHEMA: wordlist

-- DROP SCHEMA IF EXISTS wordlist ;

CREATE SCHEMA IF NOT EXISTS wordlist
    AUTHORIZATION postgres;
    
-- Table: wordlist.words

-- DROP TABLE IF EXISTS wordlist.words;

CREATE TABLE IF NOT EXISTS wordlist.words
(
    word_id integer NOT NULL DEFAULT nextval('wordlist.words_id_seq'::regclass),
    word character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT word_id PRIMARY KEY (word_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS wordlist.words
    OWNER to postgres;
-- Index: word

-- DROP INDEX IF EXISTS wordlist.word;

CREATE INDEX IF NOT EXISTS word
    ON wordlist.words USING btree
    (word COLLATE pg_catalog."default" ASC NULLS LAST)
    WITH (deduplicate_items=True)
    TABLESPACE pg_default;

-- Table: wordlist.tokens (tokenized words)

-- DROP TABLE IF EXISTS wordlist.tokens;

CREATE TABLE IF NOT EXISTS wordlist.tokens
(
    token_id integer NOT NULL DEFAULT nextval('wordlist.tokens_id_seq'::regclass),
    token character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT token_id PRIMARY KEY (token_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS wordlist.tokens
    OWNER to postgres;
-- Index: token

-- DROP INDEX IF EXISTS wordlist.token;

CREATE INDEX IF NOT EXISTS token
    ON wordlist.tokens USING btree
    (token COLLATE pg_catalog."default" ASC NULLS LAST)
    WITH (deduplicate_items=True)
    TABLESPACE pg_default;

-- Table: wordlist.tokens_words (link tokens to words)

-- DROP TABLE IF EXISTS wordlist.tokens_words;

CREATE TABLE IF NOT EXISTS wordlist.tokens_words
(
    tokens_words_id integer NOT NULL DEFAULT nextval('wordlist.tokens_words_tokens_words_id_seq'::regclass),
    tokens_id integer,
    words_id integer,
    CONSTRAINT tokens_words_id PRIMARY KEY (tokens_words_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS wordlist.tokens_words
    OWNER to postgres;
-- Index: tokens_id

-- DROP INDEX IF EXISTS wordlist.tokens_id;

CREATE INDEX IF NOT EXISTS tokens_id
    ON wordlist.tokens_words USING btree
    (tokens_id ASC NULLS LAST, words_id ASC NULLS LAST)
    WITH (deduplicate_items=True)
    TABLESPACE pg_default;