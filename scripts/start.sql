CREATE TABLE messages(
    MessageID INTEGER PRIMARY KEY,
    Author TEXT,
    AuthorID INTEGER,
    DateOfMessage DATE PRIMARY KEY,
    Content TEXT
);

CREATE TABLE edits(
    MessageID INTEGER PRIMARY KEY,
    Author TEXT,
    AuthorID INTEGER,
    DateOfOriginal DATE,
    DateOfEdit DATE PRIMARY KEY,
    OriginalContent TEXT,
    EditedContent TEXT
);