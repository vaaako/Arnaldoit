CREATE TABLE "posts" (
	"id"       INTEGER,
	"date"     TEXT,
	"content"  TEXT NOT NULL,
	"filename" TEXT,
	"like"     INTEGER,
	PRIMARY KEY("id")
);