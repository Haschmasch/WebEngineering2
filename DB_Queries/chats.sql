CREATE TABLE Chats (
	Id int PRIMARY KEY,
	OfferId int REFERENCES offers(id),
	CreatorId int REFERENCES users(id),
	TimeOpened timestamptz NOT NULL
);