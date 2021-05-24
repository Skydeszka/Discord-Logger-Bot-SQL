CREATE TABLE messages(
    MessageID       TEXT NOT NULL,
    Author          TEXT,
    AuthorID        TEXT,
    DateOfMessage   DATE NOT NULL,
    Content         TEXT,
    ChannelID       INTEGER,
    PRIMARY KEY (MessageID, DateOfMessage)
);

CREATE TABLE edits(
    MessageID       TEXT NOT NULL,
    Author          TEXT,
    AuthorID        TEXT,
    DateOfOriginal  DATE,
    DateOfEdit      DATE NOT NULL,
    OriginalContent TEXT,
    EditedContent   TEXT,
    ChannelID       INTEGER,
    PRIMARY KEY (MessageID, DateOfEdit)
);

CREATE TABLE setting (
	PresetID    INTEGER NOT NULL,
	LookbackMax	INTEGER NOT NULL,
	PRIMARY KEY (PresetID AUTOINCREMENT)
);

INSERT INTO setting(LookbackMax) VALUES (100);
INSERT INTO setting(LookbackMax) VALUES (1000);
INSERT INTO setting(LookbackMax) VALUES (10);
INSERT INTO setting(LookbackMax) VALUES (100);