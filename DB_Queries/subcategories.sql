-- Table: public.subcategories

-- DROP TABLE IF EXISTS public.subcategories;

CREATE TABLE subcategories
(
    id integer primary key,
    categoryid int references categories(id),
    name character varying(50)
)