CREATE TABLE messages(
    MessageID INTEGER NOT NULL,
    Author TEXT,
    AuthorID INTEGER,
    DateOfMessage DATE NOT NULL,
    Content TEXT,
    PRIMARY KEY (MessageID, DateOfMessage)
);

CREATE TABLE edits(
    MessageID INTEGER NOT NULL,
    Author TEXT,
    AuthorID INTEGER,
    DateOfOriginal DATE,
    DateOfEdit DATE NOT NULL,
    OriginalContent TEXT,
    EditedContent TEXT,
    PRIMARY KEY (MessageID, DateOfEdit)
);