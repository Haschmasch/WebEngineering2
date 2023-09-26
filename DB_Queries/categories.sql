-- Table: public.categories

-- DROP TABLE IF EXISTS public.categories;

CREATE TABLE categories
(
    id integer NOT NULL,
    name character varying(50)
    CONSTRAINT categories_pkey PRIMARY KEY (id)
)