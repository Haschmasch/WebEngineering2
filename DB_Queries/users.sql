-- Table: public.users

-- DROP TABLE IF EXISTS public.users;

CREATE TABLE users
(
    id integer NOT NULL,
    name character varying(150) NOT NULL,
    email character varying(200) NOT NULL,
    passwordhash text NOT NULL,
    phonenumber text,
    CONSTRAINT users_pkey PRIMARY KEY (id),
    CONSTRAINT ue_users UNIQUE (name, email)
)