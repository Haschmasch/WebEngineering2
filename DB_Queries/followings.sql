-- Table: public.followings

-- DROP TABLE IF EXISTS public.followings;

CREATE TABLE followings
(
    id integer primary key,
    offerid integer REFERENCES offers (id),
    userid integer REFERENCES users (id)
);