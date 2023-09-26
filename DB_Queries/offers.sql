-- Table: public.offers

-- DROP TABLE IF EXISTS public.offers;

CREATE TABLE offers
(
    id integer PRIMARY KEY,
    title character varying(200),
    categoryid integer references categories(id),
    subcategoryid integer references subcategories(id),
    price money,
    userid integer references users(id),
    timeposted timestamp with time zone,
    timeclosed timestamp with time zone,
    place text,
    currency character varying(30),
    CONSTRAINT chk_price CHECK (price::numeric > 0.00)
);